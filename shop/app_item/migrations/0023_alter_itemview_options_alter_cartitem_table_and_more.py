# Generated by Django 4.0 on 2022-09-16 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0022_alter_cart_table_alter_cartitem_table_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemview',
            options={'ordering': ['created']},
        ),
        migrations.AlterModelTable(
            name='cartitem',
            table='app_items_in_cart',
        ),
        migrations.AlterModelTable(
            name='itemview',
            table='app_views',
        ),
    ]
