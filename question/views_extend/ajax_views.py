# 提取出 ajax 响应函数


import json
from django.http import HttpResponse
from question.views_extend.func import add_count
from question.models import Question, User


# 响应登录的 ajax
def ajax_login(request):
    login_info = {
        'correct_logon': False,
    }

    username, password = request.POST['username'], request.POST['password']
    username_db = User.objects.filter(username=username)

    if len(username_db) > 0:
        user_db, password_db = username_db[0].username, username_db[0].password

        if password_db == password:
            login_info['correct_logon'] = True
            request.session['user'] = user_db
            return HttpResponse(json.dumps(login_info))

    return HttpResponse(json.dumps(login_info))


# 响应登出的 ajax
def ajax_logout(request):
    del request.session['user']
    return HttpResponse('success')


# 保密性设置，使用 ajax 来确认答案是否正确
def ajax_confirm_answer(request):
    choice = request.POST['choice']
    question_num = request.POST['question_num']
    answer = Question.objects.get(question_num=question_num).answer

    if choice == answer:
        if 'user' in request.session.keys():
            add_count(request.session['user'], question_num, True)
        return HttpResponse(json.dumps(dict(is_correct=True)))
    else:
        if 'user' in request.session.keys():
            add_count(request.session['user'], question_num, False)
        return HttpResponse(json.dumps(dict(is_correct=False, answer=answer)))


# 排名页面异步获取用户做题信息
def ajax_ranking(request):
    user_obj_list = User.objects.all()
    user_data_list = []

    for user in user_obj_list:
        user_data_list.append([user.user, user.right_count, user.total_count])

    return HttpResponse(json.dumps(user_data_list))
