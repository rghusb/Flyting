from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

# from . import forms
from . import models

from django.contrib.auth import get_user_model
CustomUser = get_user_model()

# Create your views here.

# CHECK CONTEXT DATA
class ArticleListView(SelectRelatedMixin, generic.ListView):
    model = models.Article
    select_related = ("customuser", "category")


class ArticleDetailView(SelectRelatedMixin, generic.DetailView):
    model = models.Article
    select_related = ("customuser", "category")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            id__iexact=self.kwargs.get("pk")
        )


class CreateArticleView(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('header','sub_header','message','category')
    model = models.Article

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Not sure if the line below is correct. Don't know if custom user translates to auth_user
        # get_user(self.request)
        self.object.customuser = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteArticleView(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Article
    select_related = ("customuser", "category")
    success_url = reverse_lazy("Articles:articles-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(customuser__id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)
