# Generated by Django 4.2.4 on 2023-08-09 20:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0008_alter_loan_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amortization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(limit_value=0, message='intial balance must greater or equal to 0')], verbose_name='intial balance amount')),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(limit_value=0, message='payment must greater or equal to 0')], verbose_name='payment amount')),
                ('interset_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(limit_value=0, message='interset must greater or equal to 0')], verbose_name='interset amount')),
                ('principal_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(limit_value=0, message='principal must greater or equal to 0')], verbose_name='principal amount')),
                ('ending_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(limit_value=0, message='ending balance must greater or equal to 0')], verbose_name='ending balance amount')),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amortizations', to='loans.loan', verbose_name='loan')),
            ],
            options={
                'verbose_name': 'amortization',
                'verbose_name_plural': 'amortizations',
                'db_table': 'amortizations',
            },
        ),
    ]