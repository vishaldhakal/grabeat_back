# Generated by Django 3.2.6 on 2023-01-26 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500)),
                ('phone_no', models.CharField(blank=True, max_length=500)),
                ('email', models.CharField(blank=True, max_length=500)),
                ('feedback', models.TextField(blank=True)),
            ],
        ),
    ]