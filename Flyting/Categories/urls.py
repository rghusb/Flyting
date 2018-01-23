from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'Categories'

urlpatterns = [
    path("new/", views.CreateCategoryView.as_view(), name="create"),
    path("posts/in/<slug:slug>/",views.DetailCategoryView.as_view(),name="detail"),
]
