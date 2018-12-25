function login_check() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === "Username" || username === '') {
        document.getElementsByClassName("error-msg")[0].style.visibility = "visible";
        document.getElementById("error-msg-text").innerText = "用户名不能为空";
    } else {
        if (password === '') {
            document.getElementsByClassName("error-msg")[0].style.visibility = "visible";
            document.getElementById('error-msg-text').innerText = '密码不能为空';
        } else {
            confirm_login(username, password);
        }
    }
}

function confirm_login(username, password) {
    $.ajax({
        url: login_ajax_parms['login_ajax_url'],
        type: "post",
        data: {'username': username, 'password': password},
        success: function (args) {
            const json = jQuery.parseJSON(args);

            if (json['correct_logon']) {
                location = login_ajax_parms['location_url'];
            } else {
                document.getElementsByClassName("error-msg")[0].style.visibility = "visible";
                document.getElementById('error-msg-text').innerText = '用户名或密码错误';
            }
        }
    });
}

function logout() {
    $.ajax({
        url: login_ajax_parms['logout_ajax_url'],
        type: "post",
        success: function () {
            const re = /space/;
            const location_url = login_ajax_parms['location_url'];
            const result = re.exec(location_url);

            if (result) location = login_ajax_parms['index_url'];
            else location = location_url;
        }
    });
}

$(document).ready(function () {
    $("#login-btn").click(function () {
        login_check();
    });

    $("#logout").click(function () {
        logout();
    });
});
