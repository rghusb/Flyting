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
    question = models.CharField(max_length=255, blank=False, default="Article-Question")
    sub_header = models.CharField(max_length=255, blank=False, default="Article-Subheader")
    message = models.TextField()
    message_html = models.TextField(editable=False)
    category = models.ForeignKey(Category, related_name="articles",null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        # self.choices.create(choice_text="Yes")
        # self.choices.create(choice_text="No")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "Articles:article-detail",
            kwargs={
                "pk": self.pk,
            }
        )

    def get_total_votes(self):
        choices_set = self.choices.all()
        total = 0
        for cur in choices_set:
            total+=cur.votes
        return total

    class Meta:
        ordering = ["-created_at"]

class Choice(models.Model):
    article = models.ForeignKey(Article, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.article.question + " ==> " + self.choice_text + " ==> " + str(self.id)

    def vote_percentage(self):
        choices_set = self.article.choices.all()
        total = 0
        for cur in choices_set:
            total += cur.votes
        if total == 0:
            return "0.0%"
        return str(round((self.votes / total)*100, 1)) + "%"

    def all_vote_percentages(self):
        choices_set = self.article.choices.all()
        choices_percentage_list = []
        for cur in choices_set:
            choices_percentage_list.append(cur.vote_percentage())
        return choices_percentage_list

class Vote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article.question + "=>" + self.customuser.username + "=>" + self.choice.choice_text

    class Meta:
        unique_together = ["article", "customuser"]

class Source(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    header = models.CharField(max_length=255, blank=False, default="Article-Source")
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.url
