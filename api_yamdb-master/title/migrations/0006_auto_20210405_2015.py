# Generated by Django 3.0.5 on 2021-04-05 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0005_title_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
