# Generated by Django 4.0 on 2022-10-06 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0024_remove_cartitem_item_remove_cartitem_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('red', ''), ('orange', ''), ('yellow', ''), ('green', ''), ('blue', ''), ('magenta', ''), ('white', ''), ('black', ''), ('grey', '')], max_length=10, null=True, verbose_name='цвет товара'),
        ),
    ]
