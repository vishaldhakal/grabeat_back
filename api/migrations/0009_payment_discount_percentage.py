# Generated by Django 3.2.6 on 2022-11-23 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20221123_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='discount_percentage',
            field=models.IntegerField(default=0),
        ),
    ]
