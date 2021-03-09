function passwordVisibility(clicked_id){
    var password = document.getElementById(clicked_id);

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


function passwordVisibilityMultiple(clicked_id){
    clicked_id.forEach(visible);

    function visible(item){
        var password = document.getElementById(item);

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
}
