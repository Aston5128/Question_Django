# 提取非页面相应函数


from django.shortcuts import get_object_or_404
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
num_of_ques = Question.objects.count()


# 提取 index(request) 和 ques(request) 公共部分
def index_ques_view(num):
    question = get_object_or_404(Question, pk=num)
    context = dict(question_num=question.question_num,
                   question_type=QUESTION_TYPE_DICT[question.question_type],
                   num_of_ques=num_of_ques,
                   question_text=question.question_text,
                   choice_a=question.choice_a,
                   choice_b=question.choice_b,
                   choice_c=question.choice_c,
                   choice_d=question.choice_d,
                   answer=question.answer,
                   difficulty=question.difficulty)
    return context


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
    if not count:
        user = User.objects.get(username=username)
        question = Question.objects.get(question_num=question_num)
        temp_count = Count(is_true=is_true,
                           username=user, question_num=question)

        user.total_count = user.total_count + 1
        user.right_count = user.right_count + is_true

        print(user.user, user.total_count, user.right_count)

        user.save()
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
