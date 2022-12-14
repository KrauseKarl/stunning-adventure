# Generated by Django 4.0 on 2022-08-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0011_remove_comment_user_comment_session_alter_item_tag'),
        ('app_user', '0006_alter_profile_review_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='review_items',
            field=models.ManyToManyField(blank=True, related_name='items', to='app_item.Item'),
        ),
    ]
