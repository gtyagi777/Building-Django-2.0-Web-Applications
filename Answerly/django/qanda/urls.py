from django.urls import path

from . import views

app_name = 'qanda'

urlpatterns = [
    path('base', views.BaseView.as_view(), name='BaseView'),
    path('ask', views.AskQuestionView.as_view(), name='ask'),
    path('q/<int:pk>', views.QuestionDetailView.as_view(), name="question_detail"),
]