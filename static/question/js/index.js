function go_to() {
    let ques_num = $('#ques_num').val();
    if (parseInt(ques_num) >= 1 && parseInt(ques_num) <= 3436) {
        location = '/question/' + ques_num;
    }
}
$(document).ready(function() {
    $('#go-to').click(function() {
        go_to();
    });

    $('#ques_num').bind('keypress', function (event) {
        if (event.keyCode === 13) {
            go_to();
        }
    });
});
