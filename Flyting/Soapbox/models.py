from django.conf import settings
from django.urls import reverse
from django.db import models

import misaka
import time

from Articles.models import Article

from django.contrib.auth import get_user_model
CustomUser = get_user_model()


# Create your models here.

class Soapbox(models.Model):
    customuser = models.ForeignKey(CustomUser, related_name="user_soapboxes", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="art_soapboxes", blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=time.strftime("%Y-%m-%d %H:%M"))
    message = models.TextField()
    message_html = models.TextField(editable=False)
    team = models.CharField(max_length=100, default="None")
    points = models.IntegerField(default=0)

    def __str__(self):
        return "SoapBox(pk=" + str(self.id) + ") created at: " + str(self.created_at) + " ==> " + str(self.article.question)

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "Soapbox:soapbox-art-list",
            kwargs={
                "art_pk": self.article.pk,
            }
        )

    class Meta:
        ordering = ["-points"]

class Rebuttal(Soapbox):
    parent = models.ForeignKey(Soapbox, related_name="parent_soapbox_rebuttals", on_delete=models.CASCADE)
    parent_rebuttal = models.ForeignKey('self', related_name="children", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Rebuttal created at: " + str(self.created_at) + " ==> " + str(self.article.question)

    def get_absolute_url(self):
        return reverse(
            "Soapbox:soapbox-detail",
            kwargs={
                "pk": self.parent.id,
            }
        )

class SoapboxVote(models.Model):
    soapbox = models.ForeignKey(Soapbox, on_delete=models.CASCADE)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        pass

    class Meta:
        unique_together = ["soapbox", "customuser"]

class RebuttalVote(models.Model):
    rebuttal = models.ForeignKey(Rebuttal, on_delete=models.CASCADE)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        pass

    class Meta:
        unique_together = ["rebuttal", "customuser"]
