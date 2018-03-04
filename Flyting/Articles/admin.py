from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Article)
admin.site.register(models.Choice)
admin.site.register(models.Vote)
admin.site.register(models.Source)
