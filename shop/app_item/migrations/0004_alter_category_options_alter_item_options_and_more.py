# Generated by Django 4.0 on 2022-08-18 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_item', '0003_item_limited_edition'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title'], 'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['created'], 'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to='category', verbose_name='иконка'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=100, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app_item.category', verbose_name='категория'),
        ),
        migrations.AlterField(
            model_name='item',
            name='comments',
            field=models.SmallIntegerField(default=0, verbose_name='комментарии'),
        ),
        migrations.AlterField(
            model_name='item',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='item/%Y/%m/%d', verbose_name='изображение'),
        ),
        migrations.AlterField(
            model_name='item',
            name='is_available',
            field=models.BooleanField(default=False, verbose_name='в наличии'),
        ),
        migrations.AlterField(
            model_name='item',
            name='limited_edition',
            field=models.BooleanField(default=False, verbose_name='ограниченный тираж'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10, verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='item',
            name='reviews',
            field=models.SmallIntegerField(default=0, verbose_name='просмотры'),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=100, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='item',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата обновления'),
        ),
    ]
