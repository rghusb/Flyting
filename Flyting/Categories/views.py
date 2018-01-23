from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from . import models

class CreateCategoryView(LoginRequiredMixin, generic.CreateView):
    fields = ("name",)
    model = models.Category

class DetailCategoryView(generic.DetailView):
    model = models.Category
