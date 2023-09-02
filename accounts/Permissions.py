from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_migrate
from accounts.models import CustomUser
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from store.models import Product



def set_user_group(user, group_name):
    group = Group.objects.get(name=group_name)
    user.groups.add(group)
    user.save()
    return user


def set_permssion_for_group(group_name, permission_name):
    group = Group.objects.get(name=group_name)
    permission = Permission.objects.get(name=permission_name)
    group.permissions.add(permission)
    group.save()
    return group


class CanEditProducts(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.has_perm('store.can_change_products')
    
class CanEditUsers(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('accounts.can_edit_products')
    
    
class AllowGetWithoutAuthentication(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated
    
class isSupervisor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Supervisor').exists()