function showPassword() {
    var x = document.getElementById('password');
    if (x.type === 'password') {
        x.type = 'text';
    } else {
        x.type = 'password'
    }
};

function showPassword2() {
    var x = document.getElementById('re_password');
    if (x.type === 'password') {
        x.type = 'text';
    } else {
        x.type = 'password'
    }
}

/*
(function($) {

    $(".toggle-password").click(function() {

        $(this).toggleClass("zmdi-eye zmdi-eye-off");
        var input = $($(this).attr("toggle"));
        if (input.attr("type") == "password") {
          input.attr("type", "text");
        } else {
          input.attr("type", "password");
        }
    });
})(jQuery);
*/