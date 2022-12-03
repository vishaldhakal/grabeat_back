# Generated by Django 3.2.6 on 2022-12-03 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20221203_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drinkspurchase',
            name='metric',
            field=models.CharField(choices=[('Ml', 'Ml'), ('Beer Bootles', 'Beer Bootles'), ('Soft Drink Bottles [0.5 Ltr]', 'Soft Drink Bottles [0.5 Ltr]'), ('Soft Drink Bottles [1 Ltr]', 'Soft Drink Bottles [1 Ltr]'), ('Soft Drink Bottles [1.5 Ltr]', 'Soft Drink Bottles [1.5 Ltr]'), ('Soft Drink Bottles [2 Ltr]', 'Soft Drink Bottles [2 Ltr]')], default='Ml', max_length=100),
        ),
        migrations.AlterField(
            model_name='drinksstock',
            name='metric',
            field=models.CharField(choices=[('Ml', 'Ml'), ('Beer Bootles', 'Beer Bootles'), ('Beer Bootles', 'Beer Bootles')], default='Ml', max_length=100),
        ),
    ]