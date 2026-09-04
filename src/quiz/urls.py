from django.urls import path

from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.exam_list, name="exam_list"),
    path("exam/<int:pk>/", views.exam_detail, name="exam_detail"),
    path("question/new/", views.question_create, name="question_create"),
]