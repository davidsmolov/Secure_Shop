# Generated by Django 4.2.4 on 2023-08-26 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_change_products', 'Can change products')]},
        ),
    ]
