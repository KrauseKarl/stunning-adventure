# Generated by Django 4.0 on 2022-09-13 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0016_order_ordered_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', to='app_item.OrderItem'),
        ),
    ]