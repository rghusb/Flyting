from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'Accounts'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="Accounts/login.html"),name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("profile/<int:pk>", views.ProfileDetailView.as_view(), name="profile_detail")
]
