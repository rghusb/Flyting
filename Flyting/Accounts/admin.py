from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Accounts import models

class CustomUserAdmin(UserAdmin):
    model = models.CustomUser

    extra_customuser_fields = ('followers',)

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': extra_customuser_fields}),
    )

admin.site.register(models.CustomUser, CustomUserAdmin)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'profile'

# Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline, )

# Re-register UserAdmin
#admin.site.unregister(User)
#admin.site.register(CustomUser, UserAdmin)
