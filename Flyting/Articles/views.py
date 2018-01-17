from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class ArticleHome(TemplateView):
    template_name = "Articles/article_home.html"
