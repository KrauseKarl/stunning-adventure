# Generated by Django 4.0 on 2022-10-02 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0009_alter_profile_review_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]