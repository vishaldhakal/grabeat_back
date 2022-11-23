# Generated by Django 3.2.6 on 2022-11-23 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_payment_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order Placed', 'Order Placed'), ('Order Completed', 'Order Completed'), ('Order Paid', 'Order Paid'), ('Order Canceled', 'Order Canceled')], default='Order Placed', max_length=400),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid'), ('Payment Canceled', 'Payment Canceled')], default='Unpaid', max_length=400),
        ),
    ]