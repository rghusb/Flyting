from django.conf import settings
from django.urls import reverse
from django.db import models

import misaka

from Articles.models import Article

from django.contrib.auth import get_user_model
CustomUser = get_user_model()


# Create your models here.

class Soapbox(models.Model):
    customuser = models.ForeignKey(CustomUser, related_name="soapboxes", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="articles", blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    points = models.IntegerField(default=0)

    def __str__(self):
        return "SoapBox created at: " + str(self.created_at)

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "Soapbox:soapbox-detail",
            kwargs={
                "pk": self.pk,
            }
        )

    class Meta:
        ordering = ["-points"]
