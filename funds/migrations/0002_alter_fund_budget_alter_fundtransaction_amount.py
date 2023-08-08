# Generated by Django 4.2.4 on 2023-08-08 18:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fund',
            name='budget',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(limit_value=0, message='total fund budget can not be less than 1')], verbose_name='budget'),
        ),
        migrations.AlterField(
            model_name='fundtransaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(limit_value=1, message='transaction amount must be greater than 1')], verbose_name='amount'),
        ),
    ]
