from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from accounts.jwt import CustomJWTAuthentication
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer, CartIteReadSerializer, CartReadSerializer, CartItemSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from accounts.jwt import extract_info_from_jwt
from accounts.models import CustomUser
from accounts.Permissions import CanEditProducts, AllowGetWithoutAuthentication # import the permission class


@permission_classes([CanEditProducts, AllowGetWithoutAuthentication])

class ProductsViews(APIView):
    serializer_class = ProductSerializer
    def get(self, request):
        id = request.query_params.get('id')
        if id:
            try:
                product = Product.objects.get(id=id)
                serializer = self.serializer_class(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({"error":f"Product with id {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.all()
            serializer = self.serializer_class(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()              
            return Response("success", status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request):
        id = request.query_params.get('id')
        if id:
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                return Response({"error":f"Product with id {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({"error":f"Product with id {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"id is required"},status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        id = request.query_params.get('id')
        if id:
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                return Response({"error":f"Product with id {id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
            product.delete()
            return Response({"success":f"Product with id {id} deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"id is required"},status=status.HTTP_400_BAD_REQUEST)

        
        
@permission_classes([IsAuthenticated])
class CartsViews(APIView):
    serializer_class = CartSerializer
    def get(self, request):
        try:
            cart = Cart.objects.get(owner = request.user, completed=False)
            serializer = CartReadSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error":f"User {request.user} Doesnt have a cart"}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, *args, **kwargs):
        user = request.user
        request.data['owner'] = CustomUser.objects.get(email=user).id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                cart = serializer.save()
                return Response(f"{cart} has been created", status=status.HTTP_201_CREATED)
            except IntegrityError: #whats the error? #a: cart already exists for user 
                return Response({"error":"Cart already exists"}, status=status.HTTP_409_CONFLICT)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            cart = Cart.objects.get(owner=request.user, completed=False)
        except Cart.DoesNotExist:
            return Response({"error":f"User {request.user} Doesnt have a cart yet"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(cart, data=request.data, partial=True)
        if serializer.is_valid():
            cart = serializer.update(cart, serializer.validated_data)
            return Response(f'{cart} Has been updated', status=status.HTTP_200_OK)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            cart = Cart.objects.get(owner=request.user, completed=False)
        except Cart.DoesNotExist:
            return Response({"error":f"User {request.user} Doesnt have a cart yet"}, status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        return Response({"success":f"{request.user}'s cart was deleted"}, status=status.HTTP_204_NO_CONTENT)