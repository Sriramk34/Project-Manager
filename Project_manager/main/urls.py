from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="home"),
    path("", views.empty),
    path("manage/",  views.manage, name="manage"),
    path("login/", views.login_site, name="login"),
    path("tasks/", views.assigned_tasks, name="tasks"),
    path("progress/", views.progress, name="progress")
]

