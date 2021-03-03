function passwordVisibility(){
    var password = document.getElementById("password");
    var show_password = document.getElementById("show-password");
    var hide_password = document.getElementById("hide-password");

    if (password.type == "password"){
        password.type = "text";
        hide_password.style.display = "flex";
        show_password.style.display = "none";
    }
    else{
        password.type = "password";
        hide_password.style.display = "none";
        show_password.style.display = "flex";
    }
}