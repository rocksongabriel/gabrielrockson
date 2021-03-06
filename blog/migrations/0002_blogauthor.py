# Generated by Django 3.2.6 on 2021-08-09 01:02

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0023_add_choose_permissions'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Enter the full name of the author', max_length=50, verbose_name='Full Name')),
                ('description', wagtail.core.fields.RichTextField(help_text='Enter a brief description about the author', verbose_name='Description of Author')),
                ('twitter', models.URLField(help_text="Input the the link to the author's twitter handle", verbose_name='Twitter Handle')),
                ('email', models.EmailField(help_text='Enter the email address of the author', max_length=500, verbose_name='Email Address')),
                ('avatar', models.ForeignKey(help_text='Upload an image of the author', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Blog Author',
                'verbose_name_plural': 'Blog Authors',
            },
        ),
    ]
