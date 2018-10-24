function login_check() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === "Username") {
        document.getElementsByClassName("error-msg")[0].style.visibility = "visible";
        document.getElementById("error-msg-text").innerText = "用户名未输入";
    } else {
        if (password === '') {
            document.getElementsByClassName("error-msg")[0].style.visibility = "visible";
            document.getElementById('error-msg-text').innerText = '密码不能为空';
        } else {
            confirm_login(username, password);
        }
    }
}

$(document).ready(function () {
   $("#login-btn").click(function () {
        login_check();
    });

   $("#logout").click(function () {
        logout();
   });
});
