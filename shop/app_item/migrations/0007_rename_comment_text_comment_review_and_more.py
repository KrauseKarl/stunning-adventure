# Generated by Django 4.0 on 2022-08-27 08:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0006_alter_itemview_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_text',
            new_name='review',
        ),
        migrations.AlterField(
            model_name='itemview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 27, 13, 12, 45, 877416)),
        ),
    ]
