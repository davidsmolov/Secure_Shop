from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import CustomUser
from rest_framework.decorators import authentication_classes, permission_classes
from accounts.Permissions import CanEditUsers, isSupervisor
from store.models import Cart
from store.serializers import CartReadSerializer
# Create your views here.


@permission_classes([CanEditUsers])      
class ActivateUser(APIView):
    def get(self,request,format=None):
        try:
            user = CustomUser.objects.get(pk=request.GET['id'])
            if user.is_active == True:
                return Response({"Error":f"User is already activated"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"Success":f"User {user} needs to be activated"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":"Wrong email"}, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request, format=None):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
            
            if user.is_active == True:
                return Response({"Error":f"User {user} is already activated"}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True

            user.save()
            return Response({"Success":f"User {user} successfully activated"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":"Wrong email"}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format=None):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
            
            if user.is_active == False:
                return Response({"Error":f"User {user} is already deactivated"}, status=status.HTTP_400_BAD_REQUEST)
            if (user.is_staff or user.is_superuser):
                user.is_staff = False
                user.is_superuser = False
            user.is_active = False

            user.save()
            return Response({"Success":f"User {user} successfully deactivated"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":"Wrong email"}, status=status.HTTP_400_BAD_REQUEST)
        
@permission_classes([CanEditUsers])      
class PromoteToSeller(APIView):
    def post(self, request, format=None):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
            group, created = Group.objects.get_or_create(name='Seller')
            if user.is_staff == True:
                return Response({"Error":f"User {user} is already a staff member"}, status=status.HTTP_400_BAD_REQUEST)
            if group in user.groups.all():
                return Response({"Error":f"User {user} is already a seller"}, status=status.HTTP_400_BAD_REQUEST)
            user.groups.add(group)
            return Response({"Success":f"User {user} successfully promoted to seller"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":"Wrong email"}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format=None):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
            group, created = Group.objects.get_or_create(name='Seller')
            if group not in user.groups.all():
                return Response({"Error":f"User {user} is not a seller"}, status=status.HTTP_400_BAD_REQUEST)
            user.groups.remove(group)
            return Response({"Success":f"User {user} successfully demoted from seller"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":"Wrong email"}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([CanEditUsers])
class PromoteToSupervisor(APIView):
    def post(self, request,format=None):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
            group, created = Group.objects.get_or_create(name='Supervisor')
            if user.is_superuser == True:
                return Response({"Error":f"User {user} is already a supervisor"}, status=status.HTTP_400_BAD_REQUEST)
            if group in user.groups.all():
                return Response({"Error":f"User {user} is already a supervisor"}, status=status.HTTP_400_BAD_REQUEST)
            user.groups.add(group)
            return Response({"Success":f"User {user} successfully promoted to supervisor"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":"Wrong email"}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, format=None):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
            group, created = Group.objects.get_or_create(name='Supervisor')
            if group not in user.groups.all():
                return Response({"Error":f"User {user} is not a supervisor"}, status=status.HTTP_400_BAD_REQUEST)
            user.groups.remove(group)
            return Response({"Success":f"User {user} successfully demoted from supervisor"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":"Wrong email"}, status=status.HTTP_400_BAD_REQUEST)
@permission_classes([isSupervisor])       
class PurchasedCarts(APIView):
    serializer_class = CartReadSerializer
    def get(self, request, format=None):
        carts = Cart.objects.filter(completed=True)
        serializer = self.serializer_class(carts, many=True)
        return Response({"Success":serializer.data}, status=status.HTTP_200_OK)