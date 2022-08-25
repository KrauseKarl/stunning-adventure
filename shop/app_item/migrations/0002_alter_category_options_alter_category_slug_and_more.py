# Generated by Django 4.0 on 2022-08-24 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=100),
        ),
    ]
