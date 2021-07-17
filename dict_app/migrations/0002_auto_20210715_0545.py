# Generated by Django 2.2 on 2021-07-15 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dict_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='search_by',
            field=models.ManyToManyField(related_name='users_searched', to='dict_app.User'),
        ),
        migrations.AddField(
            model_name='word',
            name='user_that_like_word',
            field=models.ManyToManyField(related_name='users_liked', to='dict_app.User'),
        ),
    ]
