# Generated by Django 4.0 on 2022-10-10 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0031_alter_item_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='item',
        ),
    ]