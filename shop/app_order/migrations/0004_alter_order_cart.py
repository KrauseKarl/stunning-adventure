# Generated by Django 4.0 on 2022-10-09 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_cart', '0005_alter_cart_options'),
        ('app_order', '0003_alter_order_options_order_total_sum_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_order', to='app_cart.cart'),
        ),
    ]