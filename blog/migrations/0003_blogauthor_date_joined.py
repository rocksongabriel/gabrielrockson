# Generated by Django 3.2.6 on 2021-08-09 01:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogauthor'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogauthor',
            name='date_joined',
            field=models.DateField(default=django.utils.timezone.now, help_text='Which date did this author join the team?', verbose_name='Date Joined'),
        ),
    ]
