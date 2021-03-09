$(document).ready(function(){
    $('.left-links a').click(function(){
    
        const value = $(this).attr('data-filter');
        $('.right-links').not('.'+value).hide('1000');
        $('.right-links').filter('.'+value).show('1000');
    })  
    
    // var current_password = document.getElementById("current-password").value;
    // var new_password = document.getElementById("new-password").value;
    
    // if (current_password == new_password){
    //     current_password.attr("aria-invalid", "false");
    // }
    // else if (current_password != new_password){
    //     current_password.attr("aria-invalid", "true");
    // }
})
