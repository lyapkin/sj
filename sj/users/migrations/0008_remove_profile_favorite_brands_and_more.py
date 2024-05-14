# Generated by Django 5.0.3 on 2024-05-13 08:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_producttypetranslation_name'),
        ('users', '0007_alter_favoritebrand_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='favorite_brands',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='favorite_products',
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_brands',
            field=models.ManyToManyField(through='users.FavoriteBrand', to='products.brand'),
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_products',
            field=models.ManyToManyField(through='users.FavoriteProduct', to='products.product'),
        ),
        migrations.AlterField(
            model_name='favoritebrand',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='favoriteproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
