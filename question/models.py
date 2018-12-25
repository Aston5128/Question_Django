from django.db import models


class Question(models.Model):
    question_num = models.IntegerField(primary_key=True)
    question_type = models.CharField(max_length=4)
    question_text = models.CharField(max_length=5000)
    choice_a = models.CharField(max_length=600)
    choice_b = models.CharField(max_length=600)
    choice_c = models.CharField(max_length=600)
    choice_d = models.CharField(max_length=600)
    answer = models.CharField(max_length=4)
    difficulty = models.IntegerField()


class User(models.Model):
    username = models.CharField(max_length=18, primary_key=True)
    password = models.CharField(max_length=70)
    user = models.CharField(max_length=20)
    class_name = models.CharField(max_length=40)
    right_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)


class Count(models.Model):
    username = models.ForeignKey('User', to_field='username', on_delete=models.CASCADE)
    question_num = models.ForeignKey('Question', to_field='question_num', on_delete=models.CASCADE)
    is_true = models.BooleanField()

    class Meta:
        unique_together = ('username', 'question_num')
