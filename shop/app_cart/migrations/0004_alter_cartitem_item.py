# Generated by Django 4.0 on 2022-10-02 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0024_remove_cartitem_item_remove_cartitem_user_and_more'),
        ('app_cart', '0003_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_item', to='app_item.item'),
        ),
    ]