from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = "index.html"

class LoginSuccessPage(TemplateView):
    template_name = 'login_success.html'

class LogoutSuccessPage(TemplateView):
    template_name = 'logout_success.html'
