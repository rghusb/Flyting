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
from Articles.models import Article, Choice, Vote
from Soapbox.models import Soapbox, Rebuttal, SoapboxVote, RebuttalVote

from django.contrib.auth import get_user_model
CustomUser = get_user_model()

# Create your views here.

class SoapboxDetailView(SelectRelatedMixin, generic.DetailView):
    model = models.Soapbox
    select_related = ('customuser','article',)
    template_name = "Soapbox/soapbox_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            id__iexact=self.kwargs.get("pk")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rebuttals = Rebuttal.objects.filter(parent=self.object, parent_rebuttal=None)
        print(rebuttals)
        context['soapbox_rebuttals'] = rebuttals
        return context


class SoapboxUserListView(generic.ListView):
    model = models.Soapbox
    template_name = 'Soapbox/soapbox_user_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            customuser__id__iexact=self.kwargs.get("user_pk")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['soapbox_user'] = get_object_or_404(CustomUser, pk=self.kwargs.get("user_pk"))
        return context

class SoapboxArtListView(generic.ListView):
    model = models.Soapbox
    template_name = 'Soapbox/soapbox_art_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            article__id__iexact=self.kwargs.get("art_pk")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['soapbox_article'] = get_object_or_404(Article, pk=self.kwargs.get("art_pk"))
        context['choices'] = Choice.objects.filter(article=context['soapbox_article'])
        try:
            vote = Vote.objects.filter(article=context['soapbox_article'], customuser=self.request.user)
            if vote:
                context['vote'] = vote.get().choice.choice_text
        except Exception:
            print("Get vote failed. Must be no vote")

        soapbox_array = []
        no_soapboxes = True
        for choice in context['choices']:
            qs = context['soapbox_list'].filter(team=choice.choice_text)
            soapbox_array.append({'choice':choice.choice_text, 'soapbox_set':qs})
            if qs.exists():
                no_soapboxes = False
        if not no_soapboxes:
            context['soapbox_list_array'] = soapbox_array
        return context

class SoapboxCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Soapbox
    fields = ('message',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['soapbox_article'] = get_object_or_404(Article, pk=self.kwargs.get("art_pk"))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customuser = self.request.user
        self.object.article = get_object_or_404(Article, pk=self.kwargs.get("art_pk"))
        vote = get_object_or_404(Vote, article=self.object.article, customuser=self.object.customuser)
        self.object.team = vote.choice.choice_text
        self.object.save()
        return super().form_valid(form)

class RebuttalCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Rebuttal
    template_name = "Rebuttal/rebuttal_form.html"
    fields = ('message',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get("reb_pk"):
            context['reply_bool'] = True
        cur_soapbox = None
        try:
            cur_soapbox = Soapbox.objects.get(id=self.kwargs.get("soap_pk"))
        except Soapbox.DoesNotExist:
            print("Couldn't find parent soapbox. RebuttalCreateView")
        context['soapbox'] = cur_soapbox
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customuser = self.request.user
        self.object.parent = get_object_or_404(Soapbox, pk=self.kwargs.get("soap_pk"))
        self.object.article = get_object_or_404(Article, pk=self.object.parent.article.id)
        vote = get_object_or_404(Vote, article=self.object.article, customuser=self.object.customuser)
        self.object.team = vote.choice.choice_text
        try:
            self.object.parent_rebuttal = get_object_or_404(Rebuttal, pk=self.kwargs.get("reb_pk"))
        except Exception:
            print("No Parent Rebuttal")
        self.object.save()
        return super().form_valid(form)

class ConvincedView(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("Soapbox:soapbox-art-list", kwargs={"art_pk": self.sb.article.id})

    def get(self, request, *args, **kwargs):
        self.sb = get_object_or_404(models.Soapbox, pk=self.kwargs.get("soap_pk"))
        soapbox_team = self.sb.team
        try:
            cur_vote = Vote.objects.filter(customuser=self.request.user, article=self.sb.article)
            cur_vote_team = cur_vote.get().choice.choice_text
            if (soapbox_team == cur_vote_team):
                print("Same team already")
                return super().get(request, *args, **kwargs)
            else:
                cur_choice = Choice.objects.get(article=self.sb.article, choice_text=cur_vote_team)
                new_choice = Choice.objects.get(article=self.sb.article, choice_text=soapbox_team)
                cur_choice.votes -= 1
                new_choice.votes += 1
                cur_vote.update(choice=new_choice)
                cur_vote.get().save()
                cur_choice.save()
                new_choice.save()
                print("You've switched teams")
        except Exception:
            print("Vote likely doesn't exist. ConvincedView")
        return super().get(request, *args, **kwargs)

@login_required
def UpvoteView(request):
    soapbox_id = request.GET.get('soapbox_id')
    data = {
        'div_edit': "",
        'new_total': 'New Total Error',
    }
    if request.GET and request.user:
        soapbox = get_object_or_404(models.Soapbox, pk=soapbox_id)
        try:
            vote = SoapboxVote.objects.filter(customuser=request.user, soapbox=soapbox).get()
            if vote.value == 1:
                print("Already upvoted")
                vote.value = 0
                vote.save()
                soapbox.points -= 1
            elif vote.value == 0:
                print("Currently neutral")
                vote.value = 1
                vote.save()
                soapbox.points += 1
            elif vote.value == -1:
                print("Already downvoted")
                vote.value = 1
                vote.save()
                soapbox.points += 2
        except Exception:
            print("No vote found")
            SoapboxVote.objects.create(customuser=request.user, soapbox=soapbox, value=1)
            soapbox.points += 1

        soapbox.save()
        data['div_edit'] = "." + soapbox_id
        data['new_total'] = soapbox.points
    return JsonResponse(data)

@login_required
def DownvoteView(request):
    soapbox_id = request.GET.get('soapbox_id')
    data = {
        'div_edit': "",
        'new_total': 'New Total Error',
    }
    if request.GET and request.user:
        soapbox = get_object_or_404(models.Soapbox, pk=soapbox_id)
        try:
            vote = SoapboxVote.objects.filter(customuser=request.user, soapbox=soapbox).get()
            if vote.value == 1:
                print("Already upvoted")
                vote.value = -1
                vote.save()
                soapbox.points -= 2
            elif vote.value == 0:
                print("Currently neutral")
                vote.value = -1
                vote.save()
                soapbox.points -= 1
            elif vote.value == -1:
                print("Already downvoted")
                vote.value = 0
                vote.save()
                soapbox.points += 1
            else:
                print("Something has gone wrong")
        except Exception:
            print("No vote found")
            SoapboxVote.objects.create(customuser=request.user, soapbox=soapbox, value=-1)
            soapbox.points -= 1

        soapbox.save()
        data['div_edit'] = "." + soapbox_id
        data['new_total'] = soapbox.points
    return JsonResponse(data)

@login_required
def RebuttalUpvoteView(request):
    rebuttal_id = request.GET.get('rebuttal_id')
    data = {
        'div_edit': "",
        'new_total': 'New Total Error',
    }
    if request.GET and request.user:
        rebuttal = get_object_or_404(Rebuttal, pk=rebuttal_id)
        try:
            vote = RebuttalVote.objects.filter(customuser=request.user, rebuttal=rebuttal).get()
            if vote.value == 1:
                print("Already upvoted")
                vote.value = 0
                vote.save()
                rebuttal.points -= 1
            elif vote.value == 0:
                print("Currently neutral")
                vote.value = 1
                vote.save()
                rebuttal.points += 1
            elif vote.value == -1:
                print("Already downvoted")
                vote.value = 1
                vote.save()
                rebuttal.points += 2
        except Exception:
            print("No vote found")
            RebuttalVote.objects.create(customuser=request.user, rebuttal=rebuttal, value=1)
            rebuttal.points += 1

        rebuttal.save()
        data['div_edit'] = "." + rebuttal_id
        data['new_total'] = rebuttal.points
    return JsonResponse(data)

@login_required
def RebuttalDownvoteView(request):
    print("here")
    rebuttal_id = request.GET.get('rebuttal_id')
    data = {
        'div_edit': "",
        'new_total': 'New Total Error',
    }
    if request.GET and request.user:
        rebuttal = get_object_or_404(Rebuttal, pk=rebuttal_id)
        try:
            vote = RebuttalVote.objects.filter(customuser=request.user, rebuttal=rebuttal).get()
            if vote.value == 1:
                print("Already upvoted")
                vote.value = -1
                vote.save()
                rebuttal.points -= 2
            elif vote.value == 0:
                print("Currently neutral")
                vote.value = -1
                vote.save()
                rebuttal.points -= 1
            elif vote.value == -1:
                print("Already downvoted")
                vote.value = 0
                vote.save()
                rebuttal.points += 1
            else:
                print("Something has gone wrong")
        except Exception:
            print("No vote found")
            RebuttalVote.objects.create(customuser=request.user, rebuttal=rebuttal, value=-1)
            rebuttal.points -= 1

        rebuttal.save()
        data['div_edit'] = "." + rebuttal_id
        data['new_total'] = rebuttal.points
    return JsonResponse(data)
