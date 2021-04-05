# Generated by Django 3.0.5 on 2021-04-04 18:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0002_auto_20210404_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(help_text='Use the following format: <YYYY>', validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(2021)]),
        ),
    ]