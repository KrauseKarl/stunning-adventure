# Generated by Django 4.0 on 2022-09-16 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0021_rename_order_cart_rename_orderitem_cartitem_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cart',
            table='app_carts',
        ),
        migrations.AlterModelTable(
            name='cartitem',
            table='app_cart_items',
        ),
        migrations.AlterModelTable(
            name='category',
            table='app_categories',
        ),
        migrations.AlterModelTable(
            name='comment',
            table='app_comments',
        ),
        migrations.AlterModelTable(
            name='image',
            table='app_images',
        ),
        migrations.AlterModelTable(
            name='item',
            table='app_items',
        ),
        migrations.AlterModelTable(
            name='tag',
            table='app_tags',
        ),
    ]
