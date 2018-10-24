import json
from django.shortcuts import render
from django.http import Http404, HttpResponse
from question.models import Question, User, Count


# 科目对应字典
QUESTION_TYPE_DICT = {
    'J': '数据结构',
    'K': '数据库原理',
    'W': '网络',
    'R': '软件工程',
    'Z': '操作系统',
    'C': '应用基础',
    'D': '多媒体技术',
    'Y': '硬件',
    'H': '移动互联应用',
    'L': '离散数学',
    'S': '数据表示和计算',
    'Q': '软件知识产权',
    '1': 'C语言',
    '2': 'C++',
    '3': 'Java',
    '4': 'VB',
    '5': 'VFP',
    '6': 'C#',
}


# 字典生成器
def generate_context(**kwargs):
    return dict(kwargs)


# 对错题提醒
def user_record(sess, question_num):
    user_info_list = {}
    if 'user' in sess.keys():
        user = User.objects.filter(username=sess['user'])[0].user
        user_info_list['user'] = user

        count = Count.objects.filter(username=sess['user'], question_num=question_num)

        if len(count):
            user_info_list['is_visited'] = count[0].is_true
        else:
            user_info_list['is_visited'] = -1
    else:
        user_info_list['user'] = ''
        user_info_list['is_visited'] = -2

    return user_info_list


# 对错题记录
def add_count(username, question_num, is_true):
    count = Count.objects.filter(username=username, question_num=question_num)
    if len(count) == 0:
        user = User.objects.get(username=username)
        question = Question.objects.get(question_num=question_num)
        temp_count = Count(is_true=is_true, username=user, question_num=question)
        temp_count.save()


# 头衔生成器
def generate_user_title(total_count):
    if 0 <= total_count < 10:
        return '帕斯卡机械计算机'
    elif 10 <= total_count < 50:
        return 'ENIAC'
    elif 50 <= total_count < 100:
        return '冯·诺伊曼结构'
    elif 100 <= total_count < 200:
        return 'ARPA Net'
    elif 200 <= total_count < 500:
        return 'Hello, World!'
    elif 500 <= total_count < 1000:
        return 'Intel 4004/8008/8080'
    elif 1000 <= total_count < 2000:
        return 'GNU/Linux + Git'
    else:
        return 'AlphaGo'


# session 头衔生成器
def generate_session_title(sess):
    if 'user' in sess.keys():
        username = sess['user']
        total_count = Count.objects.filter(username=username).count()
        return {'user_title': generate_user_title(total_count)}
    else:
        return {}


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


# 顺序练习
def index(request):
    question = Question.objects.get(question_num=1)

    record = user_record(request.session, 1)
    user_title = generate_session_title(request.session)

    context = generate_context(question_num=question.question_num,
                               question_type=QUESTION_TYPE_DICT[question.question_type],
                               question_text=question.question_text,
                               choice_a=question.choice_a,
                               choice_b=question.choice_b,
                               choice_c=question.choice_c,
                               choice_d=question.choice_d,
                               answer=question.answer,
                               difficulty=question.difficulty)
    context.update(record)
    context.update(user_title)

    return render(request, 'question/index.html', context=context)


# 根据题号的顺序练习
def ques(request, num=1):
    if num <= 0 or num >= 3437:
        raise Http404('Page Not Found')

    question = Question.objects.get(question_num=num)

    record = user_record(request.session, question.question_num)
    user_title = generate_session_title(request.session)

    context = generate_context(question_num=question.question_num,
                               question_type=QUESTION_TYPE_DICT[question.question_type],
                               question_text=question.question_text,
                               choice_a=question.choice_a,
                               choice_b=question.choice_b,
                               choice_c=question.choice_c,
                               choice_d=question.choice_d,
                               answer=question.answer,
                               difficulty=question.difficulty)
    context.update(record)
    context.update(user_title)

    return render(request, 'question/index.html', context=context)


# 专题练习
def subject(request, subject_code, num=1):
    """

    :param request:
    :param subject_code: 题型代码
    :param num: 该题型的第几题
    :return: 响应页面
    """
    question = Question.objects.filter(question_type=subject_code)
    num_of_ques = len(question)
    question_num = question[num - 1].question_num

    if num_of_ques is 0 or num <= 0 or num > num_of_ques:
        raise Http404('Page Not Found')

    record = user_record(request.session, question_num)
    user_title = generate_session_title(request.session)

    context = generate_context(question_order=num,
                               num_of_ques=num_of_ques,
                               question_num=question_num,
                               question_type=QUESTION_TYPE_DICT[question[num - 1].question_type],
                               question_type_code=subject_code,
                               question_text=question[num - 1].question_text,
                               choice_a=question[num - 1].choice_a,
                               choice_b=question[num - 1].choice_b,
                               choice_c=question[num - 1].choice_c,
                               choice_d=question[num - 1].choice_d,
                               answer=question[num - 1].answer,
                               difficulty=question[num - 1].difficulty)
    context.update(record)
    context.update(user_title)

    return render(request, 'question/subject.html', context=context)


# 个人中心
def space(request):
    username = request.session['user']
    user = User.objects.get(username=username)
    count = Count.objects.filter(username=username)

    total_count = len(count)                                                   # 做题总数
    wrong_count = len(count.filter(is_true=0))                                 # 错题数
    right_count = total_count - wrong_count                                    # 正确数
    if total_count == 0:                                                       # 正确率
        right_rate = 0
    else:
        right_rate = int(round(right_count / total_count, 2) * 100)

    user_title = generate_user_title(total_count)

    context = generate_context(user=user.user, user_title=user_title, total_count=total_count, wrong_count=wrong_count,
                               right_count=right_count, right_rate=right_rate)

    return render(request, 'question/space.html', context=context)


# 自定义 404 页面
def page_not_found(request):
    return render(request, '404.html')
