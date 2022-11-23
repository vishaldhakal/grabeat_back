# Generated by Django 3.2.6 on 2022-11-23 04:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20221123_0415'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanclePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid'), ('Payment Canceled', 'Payment Canceled')], default='Unpaid', max_length=400)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('cancle_reason', models.TextField(blank=True)),
                ('order', models.ManyToManyField(to='api.Order')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]