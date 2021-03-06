# Generated by Django 3.2.6 on 2021-08-09 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('blog', '0003_blogauthor_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogauthor',
            name='avatar',
            field=models.ForeignKey(help_text='Upload an image of the author', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
