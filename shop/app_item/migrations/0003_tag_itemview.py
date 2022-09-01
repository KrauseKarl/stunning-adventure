# Generated by Django 4.0 on 2022-08-26 06:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0002_alter_category_options_alter_category_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ItemView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('created', models.DateTimeField(default=datetime.datetime(2022, 8, 26, 11, 14, 48, 504639))),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='app_item.item')),
            ],
        ),
    ]
