# Generated by Django 2.0.1 on 2018-03-04 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Soapbox', '0012_auto_20180225_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rebuttal',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_soapbox_rebuttals', to='Soapbox.Soapbox'),
        ),
        migrations.AlterField(
            model_name='rebuttal',
            name='soapbox_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Soapbox.Soapbox'),
        ),
        migrations.AlterField(
            model_name='soapbox',
            name='created_at',
            field=models.DateTimeField(default='2018-03-04 06:04'),
        ),
        migrations.AlterField(
            model_name='soapboxvote',
            name='soapbox',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Soapbox.Soapbox'),
        ),
    ]
