from django.conf import settings
from django.urls import reverse
from django.db import models

import misaka

from Categories.models import  Category

from django.contrib.auth import get_user_model
CustomUser = get_user_model()


class Article(models.Model):
    customuser = models.ForeignKey(CustomUser, related_name="articles",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    header = models.CharField(max_length=255, blank=False, default="Article-Header")
    sub_header = models.CharField(max_length=255, blank=False, default="Article-Subheader")
    message = models.TextField()
    message_html = models.TextField(editable=False)
    category = models.ForeignKey(Category, related_name="articles",null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "Articles:article-detail",
            kwargs={
                "pk": self.pk,
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["customuser", "message"]
