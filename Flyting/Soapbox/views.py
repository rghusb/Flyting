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

class SoapboxDetailView(SelectRelatedMixin, generic.DetailView):
    model = models.Soapbox
    select_related = ('customuser','article',)
    template_name = "SoapBox/soapbox_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            id__iexact=self.kwargs.get("pk")
        )

class SoapboxListView(generic.ListView):
    model = models.Soapbox

class SoapboxArtListView(generic.ListView):
    model = models.Soapbox

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            article__id__iexact=self.kwargs.get("art_pk")
        )

class SoapboxCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Soapbox
    fields = ('message', 'article',)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.customuser = self.request.user
        self.object.save()
        return super().form_valid(form)
