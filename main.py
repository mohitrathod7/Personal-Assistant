from flask import *
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import *
from wtforms_components import TimeField, read_only, DateRange
from wtforms.validators import *
from wtforms.fields.html5 import DateField, DateTimeField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from urllib.parse import *
from datetime import *


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
    password = db.Column(db.String(80), nullable=False)
    logged_in = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String(20), default="")
    lastname = db.Column(db.String(20), default="")
    phone = db.Column(db.Integer, unique=True, default="")
    gender = db.Column(db.String(10), nullable=False, default="Other")
    # dateofbirth = db.Column(db.Date, default="")

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])


@app.errorhandler(404)
# inbuilt function which takes error as parameter 
def not_found(e):
    return render_template("error404.html") 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)            
                update = User.query.filter_by(username=current_user.username).first()
                update.logged_in = "True"
                db.session.commit()
                return redirect(url_for('home'))
        else:
            return render_template('login.html', form=form, uname_help_block="block", display_login="block", display_logout="none", display_signup="block", display_settings="none")
    return render_template('login.html', form=form, uname_help_block="none", display_login="block", display_logout="none", display_signup="block", display_settings="none")


@app.route('/logout')
@login_required
def logout():
    update = User.query.filter_by(username=current_user.username).first()
    update.logged_in = "False"
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
            
            return redirect(url_for('settings', id='general'))
    except exc.SQLAlchemyError as e:
        return render_template('signup.html', form=form, uname_help_block="none", email_help_block="none", display_login="block", display_logout="none", display_signup="block", display_settings="none")
    
    try:
        if current_user.logged_in == "True":
            return redirect(url_for('home'))
    except:
        return render_template("signup.html", form=form, display_login="block", display_logout="none", display_signup="block", display_settings="none")


@app.route('/deleteaccount', methods=['GET'])
def deleteAccount():
    try:
        if current_user.logged_in == "True":
            # Accessing all usernames as a list and sending to list
            username_list = []
            username_raw_list = db.session.query(User.username).all()

            for i in username_raw_list:
                username_list.append(i[0])

            # Deleting user
            password = request.args.get('password')
            user = User.query.filter_by(username=current_user.username).first()
            
            if check_password_hash(user.password, password):
                db.session.delete(user)
                db.session.commit()
                print("success")
                return render_template("delete.html", display_login="none", display_logout="block", display_signup="none", display_settings="block", query="Hello "+ current_user.firstname)
            else:
                pass
            return render_template("delete.html", display_login="none", display_logout="block", display_signup="none", display_settings="block", query="Hello "+ current_user.firstname)
    except:
        return render_template("home.html", display_login="none", display_logout="block", display_signup="none", display_settings="block")


@app.route('/')
def home():
    try:
        if current_user.logged_in == "True":
            return render_template("home.html", display_login="none", display_logout="block", display_signup="none", display_settings="block", query="Hello "+ current_user.firstname)
    except:
        return render_template("home.html", display_login="block", display_logout="none", display_signup="block", display_settings="none")


@app.route('/settings/<string:id>', methods=['GET', 'POST'])
@login_required
def settings(id):
    try:
        # check current gender to display default checked gender radio button 
        if current_user.logged_in == "True":
            display_gender = current_user.gender.lower()
            
            if display_gender == "male":
                male = "checked"
                female = "unchecked"
                other = "unchecked"
            elif display_gender == "female":
                male = "unchecked"
                female = "checked"
                other = "unchecked"
            elif display_gender == "other":
                male = "unchecked"
                female = "unchecked"
                other = "checked"
            else:
                male = "unchecked"
                female = "unchecked"
                other = "checked"

            return render_template("settings/"+ id +".html", _uname=current_user.username, _fname=current_user.firstname,
                                        _lname=current_user.lastname, _email=current_user.email, _phone=current_user.phone, 
                                        _gender=current_user.gender, _male=male, _female=female, _other=other,
                                        display_login="none", display_logout="block", display_signup="none", display_settings="block",
                                        query="Hello "+str(current_user.firstname))
    except:
        return render_template("settings/"+ id +".html", display_login="block", display_logout="none", display_signup="block", display_settings="none") 


@app.route('/changeSettings/general')
@login_required
def changeSettingsGeneral():
    update = User.query.filter_by(username=current_user.username).first()

    _fname = request.args.get('firstname')
    _lname = request.args.get('lastname')
    _email = request.args.get('email')
    _phone = request.args.get('phone')
    _gender = request.args.get('gender')
    # _dateOfBirth = request.args.get('dateOfBirth')

    column = ["firstname", "lastname", "email", "phone", "gender"]
    row = [_fname, _lname, _email, _phone, _gender]

    try:
        for item in range(len(column)):
            try:
                if column[item] == "firstname":
                    update.firstname = str(row[item])
                    db.session.commit()
                elif column[item] == "lastname":
                    update.lastname = str(row[item])
                    db.session.commit()
                elif column[item] == "email":
                    update.email = str(row[item])
                    db.session.commit()
                elif column[item] == "phone":
                    update.phone = int(row[item])
                    db.session.commit()
                elif column[item] == "gender":
                    update.gender = str(row[item])
                    db.session.commit()
            except:
                print("error")
    finally:
        pass

    return redirect(url_for('settings', id="general"))


@app.route('/changeSettings/account')
@login_required
def changeSettingsAccount():
    update = User.query.filter_by(username=current_user.username).first()

    _uname = request.args.get('username')
    _lname = request.args.get('lastname')

    column = ["username", "lastname"]
    row = [_uname, _lname]

    try:
        for item in range(len(column)):
            try:
                if column[item] == "username":
                    update.firstname = str(row[item])
                    db.session.commit()
                elif column[item] == "lastname":
                    update.lastname = str(row[item])
                    db.session.commit()
            except:
                print("error")
    finally:
        pass

    return redirect(url_for('settings', id='account'))


@app.route('/changeSettings/password')
@login_required
def changeSettingsPassword():
    update = User.query.filter_by(username=current_user.username).first()
    current_password = request.args.get('current-password')
    new_password = request.args.get('new-password')

    try:
        if current_user.logged_in == "True":
            try:
                if (check_password_hash(current_user.password, str(current_password))):
                    hashed_password = generate_password_hash(new_password, method='sha256')
                    update.password = str(hashed_password)
                    db.session.commit()
                    return redirect(url_for('settings', id='password'))
                elif str(current_user.password) == str(current_password):
                    return redirect(url_for('settings', id='password'))
            except TypeError:
                return redirect(url_for('settings', id='password'))
    except:
        return redirect(url_for('settings', id='password'))


@app.route('/help', methods=['GET', 'POST'])
def help():
    try:
        if current_user.logged_in == "True":
            return render_template("help.html", display_login="none", display_logout="block", display_signup="none", display_settings="block")
    except:
        return render_template("help.html", display_login="block", display_logout="none", display_signup="block", display_settings="none")


if __name__ == '__main__': 
    app.run(debug = True)
