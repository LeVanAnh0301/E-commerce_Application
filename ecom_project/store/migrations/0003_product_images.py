# Generated by Django 4.1 on 2023-11-21 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation_reviewrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ImageField(null=True, upload_to='photos/products'),
        ),
    ]
