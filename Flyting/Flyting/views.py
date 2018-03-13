from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from Articles.models import Article

from Categories.models import Category


class HomePage(ListView):
    model = Article
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['daily_drip'] = context['object_list'][:5]

        # Iterate through categories
        # Category List

        context['politics_list'] = context['object_list'].filter(category_id=1)[:3]
        context['culture_list'] = context['object_list'].filter(category_id=2)[:3]
        context['sports_list'] = context['object_list'].filter(category_id=3)[:3]
        context['sponsored_list'] = context['object_list'][:3]
        return context

class LoginSuccessPage(TemplateView):
    template_name = 'login_success.html'

class LogoutSuccessPage(TemplateView):
    template_name = 'logout_success.html'
