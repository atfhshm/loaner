# Generated by Django 4.2.4 on 2023-08-11 12:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='loan start date'),
            preserve_default=False,
        ),
    ]
