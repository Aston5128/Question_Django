from django.urls import path
from question.views import *
from question.views_extend.ajax_views import *

urlpatterns = [
    path('', index, name='index'),
    path('question/<int:num>/', ques, name='ques'),
    path('subject/<str:subject_code>/<int:num>', subject, name='subject'),
    path('space/', space, name='space'),
    path('ranking/', rank, name='rank'),
    path('ajax_login/', ajax_login, name='ajax_login'),
    path('ajax_logout/', ajax_logout, name='ajax_logout'),
    path('ajax_confirm_answer/', ajax_confirm_answer,
         name='ajax_confirm_answer'),
    path('ajax_ranking/', ajax_ranking, name='ajax_ranking'),
]

handler404 = 'Question_Django.question.views.page_not_found'
