# Generated by Django 4.0 on 2022-08-26 12:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0003_tag_itemview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 26, 17, 29, 47, 872200)),
        ),
    ]
