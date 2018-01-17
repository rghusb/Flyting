from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'Articles'

urlpatterns = [
    path("", views.ArticleHome.as_view(), name="article-home"),
]
