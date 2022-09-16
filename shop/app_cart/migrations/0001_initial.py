# Generated by Django 4.0 on 2022-09-16 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_item', '0024_remove_cartitem_item_remove_cartitem_user_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('ordered', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_item.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_add_items', to='auth.user')),
            ],
            options={
                'verbose_name': 'выбранный товар',
                'db_table': 'app_items_in_cart',
                'ordering': ['item'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ordered', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(related_name='orders', to='app_cart.CartItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to='auth.user')),
            ],
            options={
                'verbose_name': 'заказ',
                'db_table': 'app_carts',
                'ordering': ['created'],
            },
        ),
    ]
