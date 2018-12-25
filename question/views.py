from django.shortcuts import render, get_list_or_404
from django.http import Http404
from question.views_extend.func import *  # 非页面响应函数


# 顺序练习
def index(request):
    record = user_record(request.session, 1)
    user_title = generate_session_title(request.session)
    context = index_ques_view(1)

    context.update(record)
    context.update(user_title)

    return render(request, 'question/index.html', context=context)


# 根据题号的顺序练习
def ques(request, num=1):
    record = user_record(request.session, num)
    user_title = generate_session_title(request.session)
    context = index_ques_view(num)

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
    question_list = get_list_or_404(Question, question_type=subject_code)
    num_of_subj = len(question_list)

    if num_of_subj is 0 or num <= 0 or num > num_of_subj:
        raise Http404('Page Not Found')

    question = question_list[num - 1]

    question_num = question.question_num

    record = user_record(request.session, question_num)
    user_title = generate_session_title(request.session)

    context = dict(question_order=num,
                   num_of_ques=num_of_subj,
                   question_num=question_num,
                   question_type=QUESTION_TYPE_DICT[question.question_type],
                   question_type_code=subject_code,
                   question_text=question.question_text,
                   choice_a=question.choice_a,
                   choice_b=question.choice_b,
                   choice_c=question.choice_c,
                   choice_d=question.choice_d,
                   answer=question.answer,
                   difficulty=question.difficulty)
    context.update(record)
    context.update(user_title)

    return render(request, 'question/subject.html', context=context)


# 个人中心
def space(request):
    username = request.session['user']
    user = User.objects.get(username=username)

    total_count = user.total_count  # 做题总数
    right_count = user.right_count  # 正确数
    wrong_count = total_count - right_count  # 错题数
    if total_count == 0:  # 正确率
        right_rate = 0
    else:
        right_rate = int(round(right_count / total_count, 2) * 100)

    user_title = generate_user_title(total_count)

    context = dict(user=user.user, user_title=user_title,
                   total_count=total_count, wrong_count=wrong_count,
                   right_count=right_count, right_rate=right_rate,
                   user_class_name=user.class_name)

    return render(request, 'question/space.html', context=context)


# 排名页面
def rank(request):
    username = request.session['user']
    user = User.objects.get(username=username)

    context = dict(user=user.user)

    return render(request, 'question/rank.html', context=context)


# 自定义 404 页面
def page_not_found(request):
    return render(request, '404.html')
