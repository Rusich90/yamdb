# Generated by Django 3.0.5 on 2021-04-07 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0013_title_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
