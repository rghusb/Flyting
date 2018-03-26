from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from . import models
from . import forms
from Soapbox.models import Soapbox

from django.contrib.auth import get_user_model
CustomUser = get_user_model()

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
        usr_top_soapbox = self.object.user_soapboxes.first()
        if usr_top_soapbox:
            context['user_top_soapbox'] = [usr_top_soapbox]
        return context
