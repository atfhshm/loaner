# Generated by Django 4.2.4 on 2023-08-09 18:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0005_remove_loan_yearly_interest_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='payment_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(limit_value=1, message='interest rate can not be less than 1 (%)')], verbose_name='loan payment amount'),
        ),
    ]