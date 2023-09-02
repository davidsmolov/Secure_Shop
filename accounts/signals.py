from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

from django.contrib.auth.models import Group, Permission
from .models import CustomUser

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'accounts':
        store_app_config = apps.get_app_config('store')
        can_edit_products = Permission.objects.get(
            codename='can_change_products',
            content_type__app_label=store_app_config.label
        )
        Group.objects.get_or_create(name='Seller')
        Group.objects.get_or_create(name='Supervisor')
        Group.objects.get(name='Seller').permissions.add(can_edit_products)
        Group.objects.get(name='Supervisor').permissions.add(can_edit_products)
        store_app_config = apps.get_app_config('accounts')
        can_edit_users = Permission.objects.get(
            codename='can_edit_users',
            content_type__app_label=store_app_config.label
        )
        Group.objects.get(name='Supervisor').permissions.add(can_edit_users)
        
        