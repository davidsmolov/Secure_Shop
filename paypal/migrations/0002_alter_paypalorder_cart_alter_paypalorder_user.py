# Generated by Django 4.2.3 on 2023-08-12 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_cart_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paypal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paypalorder',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.cart'),
        ),
        migrations.AlterField(
            model_name='paypalorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
