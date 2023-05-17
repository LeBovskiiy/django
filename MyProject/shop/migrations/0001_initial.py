# Generated by Django 4.1.5 on 2023-04-02 13:52

from django.db import migrations, models

import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30, verbose_name='Product category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=30, verbose_name='Product tags')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Product name')),
                ('description', models.TextField(max_length=500, verbose_name='Product discription')),
                ('price', models.IntegerField(verbose_name='Price')),
                ('image', models.ImageField(blank=True, null=True, upload_to=shop.models.user_directory_path, verbose_name='Photo')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('categories', models.ManyToManyField(blank=True, to='shop.productcategory')),
                ('tags', models.ManyToManyField(blank=True, to='shop.producttags')),
            ],
        ),
    ]
