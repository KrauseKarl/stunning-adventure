# Generated by Django 4.0 on 2022-08-27 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0009_alter_itemview_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemview',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
