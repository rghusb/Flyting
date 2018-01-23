from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "somename", "password1", "password2")
        model = models.CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"

# class ProfileCreateForm(UserCreationForm):
#     class Meta:
#         fields = ("department",)
#         model = models.Profile
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["department"].label = "Department name"
