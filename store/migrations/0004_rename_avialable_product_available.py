# Generated by Django 4.2.4 on 2023-08-26 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_cart_completed_product_avialable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='avialable',
            new_name='available',
        ),
    ]
