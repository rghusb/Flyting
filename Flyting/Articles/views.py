from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json

from braces.views import SelectRelatedMixin

# from . import forms
from . import models

from django.contrib.auth import get_user_model
CustomUser = get_user_model()


# Create your views here.

class ArticleListView(SelectRelatedMixin, generic.ListView):
    model = models.Article
    select_related = ("customuser", "category")

class ArticleDetailView(SelectRelatedMixin, generic.DetailView):
    model = models.Article
    select_related = ("customuser", "category")
    template_name = "Articles/article_detail_2.html"

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
        try:
            context['art_top_soapbox'] = [self.object.art_soapboxes.first()]
            if context['art_top_soapbox'][0] == None:
                context['art_top_soapbox'] = None
        except Exception:
            print('Article Top Soapbox Problem')
        context['sources'] = ['1','2','3']
        return context


class CreateArticleView(LoginRequiredMixin, generic.CreateView):
    fields = ('question','sub_header','message','category')
    model = models.Article

    def form_valid(self, form):
        self.object = form.save(commit=False)
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

    # Vote can only be accessed if user is logged in and hasn't voted due to how article_detail page is setup with template tags
    # def get(self, request, *args, **kwargs):
    #     if self.kwargs.get('user_id'):
    #         try:
    #             choice = get_object_or_404(models.Choice, pk=self.kwargs.get("choice_id"))
    #             models.Vote.objects.create(article=choice.article, customuser=self.request.user, choice=choice)
    #             choice.votes += 1
    #             choice.save()
    #         except Exception:
    #             print("Error in VoteRedirectView")
    #
    #     return super().get(request, *args, **kwargs)

@login_required
def VoteView(request):
    data = {
        'new_total': 'New Total Error',
    }
    if request.GET:
        print("Voting")
        try:
            choice_id = request.GET.get('choice_id')
            choice = get_object_or_404(models.Choice, pk=choice_id)
            vote = models.Vote.objects.create(article=choice.article, customuser=request.user, choice=choice)
            choice.votes += 1
            choice.save()
            data['percs'] = choice.all_vote_percentages()
            data['msg'] = choice.choice_text
            data['new_total'] = str(choice.article.get_total_votes())
        except Exception:
            data['msg'] = 'Voting Error'
            data['percs'] = ["Percentage Error",]
        print("Voted")
    return JsonResponse(data)
