from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from . import models
from . import forms

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    #second_form_class = forms.ProfileCreateForm
    success_url = reverse_lazy("login")
    template_name = "Accounts/signup.html"


class ProfileDetailView(DetailView):
    template_name = "UserProfile/profile_detail.html"
    model = models.CustomUser

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            id__iexact=self.kwargs.get("pk")
        )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context["profile_user"] = self.
        return context
