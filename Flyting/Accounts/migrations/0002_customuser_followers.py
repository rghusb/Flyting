# Generated by Django 2.0.1 on 2018-02-17 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='followers',
            field=models.IntegerField(default=0),
        ),
    ]
