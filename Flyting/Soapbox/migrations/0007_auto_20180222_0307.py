# Generated by Django 2.0.1 on 2018-02-22 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Soapbox', '0006_auto_20180222_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soapbox',
            name='created_at',
            field=models.DateTimeField(default='2018-02-22 03:07'),
        ),
    ]
