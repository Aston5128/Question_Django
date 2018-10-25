# 提取非页面相应函数


from question.models import Question, User, Count


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
