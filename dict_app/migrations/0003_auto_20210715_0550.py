# Generated by Django 2.2 on 2021-07-15 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dict_app', '0002_auto_20210715_0545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='search_by',
            new_name='searched_by',
        ),
    ]
