from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user_vote'] = models.Vote.objects.filter(article=self.object, customuser=self.request.user).get()
        except Exception:
            pass
        context['total_votes'] = self.object.get_total_votes()
        return context


class CreateArticleView(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('question','sub_header','message','category')
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


class VoteRedirectView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("Articles:article-detail", kwargs={"pk": self.kwargs.get("article_id")}) + "#QUESTION"

    def get(self, request, *args, **kwargs):
        has_voted = models.Vote.objects.filter(article__id=self.kwargs.get("article_id"), customuser__id=self.kwargs.get("user_id")).exists()

        if not has_voted:
            choice = get_object_or_404(models.Choice, pk=self.kwargs.get("choice_id"))
            models.Vote.objects.create(article=choice.article, customuser=self.request.user, choice=choice)

        return super().get(request, *args, **kwargs)
