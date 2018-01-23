from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
# from accounts.models import User


from django.contrib.auth import get_user_model
CustomUser = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    members = models.ManyToManyField(CustomUser,through="CategoryMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("Categories:detail", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class CategoryMember(models.Model):
    category = models.ForeignKey(Category, related_name="memberships", on_delete=models.CASCADE)
    customuser = models.ForeignKey(CustomUser, related_name='user_categories', on_delete=models.CASCADE)

    def __str__(self):
        return self.customuser.username

    class Meta:
        unique_together = ("category", "customuser")
