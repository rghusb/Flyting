# Generated by Django 2.0.1 on 2018-02-22 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Soapbox', '0007_auto_20180222_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soapbox',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='art_soapboxes', to='Articles.Article'),
        ),
        migrations.AlterField(
            model_name='soapbox',
            name='created_at',
            field=models.DateTimeField(default='2018-02-22 06:48'),
        ),
        migrations.AlterField(
            model_name='soapbox',
            name='customuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_soapboxes', to=settings.AUTH_USER_MODEL),
        ),
    ]
