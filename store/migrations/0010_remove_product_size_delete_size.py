# Generated by Django 4.2.3 on 2023-12-22 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_size_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
