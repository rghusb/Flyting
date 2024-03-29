# Generated by Django 2.0.1 on 2018-02-08 00:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Articles', '0006_auto_20180126_1305'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SoapBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('message_html', models.TextField(editable=False)),
                ('points', models.IntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='Articles.Article')),
                ('customuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soapboxes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
