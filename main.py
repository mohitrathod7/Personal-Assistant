from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from urllib.parse import *


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/database/database.db'


bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    logged_in = db.Column(db.String, nullable=False)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['next'] = request.args.get('next')
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)            
                update_this = User.query.filter_by(username=current_user.username).first()
                update_this.logged_in = "True"
                db.session.commit()
                return redirect(url_for('home'))
        else:
            return render_template('login.html', form=form, uname_help_block="block")
    return render_template('login.html', form=form, uname_help_block="none", display_login="block", display_logout="none", display_signup="block")


@app.route('/logout')
@login_required
def logout():
    update_this = User.query.filter_by(username=current_user.username).first()
    update_this.logged_in = "False"
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    try:
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, logged_in="True")
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('settings'))
    except exc.SQLAlchemyError as e:
        return render_template('signup.html', form=form, uname_help_block="block", display_login="block", display_logout="none", display_signup="block")

    try:
        if current_user.logged_in == "True":
            return render_template('signup.html', form=form, display_login="none", display_logout="block", display_signup="none", query="Hello")
    except:
        return render_template('signup.html', form=form, display_login="block", display_logout="none", display_signup="block")


@app.route('/')
def home():
    try:
        if current_user.logged_in == "True":
            return render_template("home.html", display_login="none", display_logout="block", display_signup="none", query="Hello "+ current_user.username)
    except:
        return render_template("home.html", display_login="block", display_logout="none", display_signup="block")


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    try:
        if current_user.logged_in == "True":
            return render_template("settings.html", display_login="none", display_logout="block", display_signup="none", query="Hello")
    except:
        return render_template("settings.html", display_login="block", display_logout="none", display_signup="block")


@app.route('/help', methods=['GET', 'POST'])
def help():
    try:
        if current_user.logged_in == "True":
            return render_template("help.html", display_login="none", display_logout="block", display_signup="none")
    except:
        return render_template("help.html", display_login="block", display_logout="none", display_signup="block")


if __name__ == '__main__': 
    app.run(debug = True)
