# Generated by Django 4.2.3 on 2023-08-05 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('can_edit_products', 'Can edit products'), ('can_edit_users', 'Can edit users')]},
        ),
    ]
