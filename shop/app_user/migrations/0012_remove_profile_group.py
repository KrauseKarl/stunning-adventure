# Generated by Django 4.0 on 2022-10-09 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0011_remove_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='group',
        ),
    ]
