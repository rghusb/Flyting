# Generated by Django 2.0.1 on 2018-02-23 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Soapbox', '0008_auto_20180222_0648'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rebuttal',
            fields=[
                ('soapbox_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Soapbox.Soapbox')),
            ],
            bases=('Soapbox.soapbox',),
        ),
        migrations.AlterField(
            model_name='soapbox',
            name='created_at',
            field=models.DateTimeField(default='2018-02-23 01:20'),
        ),
        migrations.AddField(
            model_name='rebuttal',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_soapbox', to='Soapbox.Soapbox'),
        ),
    ]
