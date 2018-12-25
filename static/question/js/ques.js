function choice_click(num) {
    const choice_list = $('.choice-label');
    for (let i = 1; i <= 4; ++i) {
        if (i === num) {
            choice_list[i - 1].id = 'choice-label-selected';
        } else {
            choice_list[i - 1].id = '';
        }
    }
}

function change_question_stat(pos, text, color) {
    let question_info_div = $('.question-info-div');
    let info_span = question_info_div[2].getElementsByTagName('span')[0];

    question_info_div[2].getElementsByTagName('div')[0].style.backgroundPosition = pos;
    info_span.innerHTML = text;
    info_span.style.color = color;
}

function confirm_answer(choice) {
    $.ajax({
        url: question_url_dict['ajax_confirm_answer'],
        type: "post",
        data: {'question_num': question_num, 'choice': choice},
        success: function (args) {
            const json = jQuery.parseJSON(args);
            let choice_list = $('.choice-label');
            if (json['is_correct']) {
                change_question_stat('0 -47px', '正确', '#28a745');
                choice_list[choice.charCodeAt(0) - 65].id = 'choice-label-correct';
                setTimeout("location = question_url_dict['next_page']", 3000);
            } else {
                change_question_stat('0 -96px', '错误', '#dc3545');
                let correct_choice = json['answer'].charCodeAt(0) - 65;
                choice_list[choice.charCodeAt(0) - 65].id = 'choice-label-wrong';
                choice_list[correct_choice].id = 'choice-label-correct';
            }
        }
    });
}

function page_jump(page) {
    if (page === -1) location = question_url_dict['pre_page'];
    else location = question_url_dict['next_page'];
}

function page_shift(page, num_of_ques) {
    if (question_order) {
        if (question_order === 1 && page === -1) alert('<(￣ ﹌ ￣)>不能往前了');
        else if (question_order === num_of_ques && page === 1) alert('<(￣ ﹌ ￣)>不能往后了');
        else page_jump(page);
    } else {
        if (question_num === '1' && page === -1) alert('<(￣ ﹌ ￣)>不能往前了');
        else if (question_num === num_of_ques.toString() && page === 1) alert('<(￣ ﹌ ￣)>不能往后了');
        else page_jump(page);
    }
}

function go_to_page(num_of_ques, code = '') {
    let page_num_input = $('#go-to');
    let page_num_str = page_num_input.val();
    if (page_num_str === '') return;

    let page_num = parseInt(page_num_str);
    if (code === '' && page_num > 0 && page_num <= num_of_ques) {
        location = '/question/' + page_num_str;
    } else if (code !== '' && page_num > 0 && page_num <= num_of_ques) {
        location = '/subject/' + code + '/' + page_num_str;
    } else {
        page_num_input.val('');
        alert('<(￣ ﹌ ￣)>别搞小破坏哦');
    }
}

$(document).ready(function () {
    $('#sub-btn').click(function () {
        const choice = $('input:radio[name="choice"]:checked').val();
        confirm_answer(choice);
    });
});
