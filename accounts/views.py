from asyncio import exceptions
import string
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
import random
from django.contrib.sites.shortcuts import get_current_site
from .utlis import Util
from .models import ResetPassword as ResetPasswordModel
# Create your views here.

class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            user.save()
            
            new_user = CustomUser.objects.get(email=serializer.validated_data['email'])
            
            current_site = get_current_site(request).domain
            relativeLink = reverse('ActivateUser')
            absurl = 'http://'+current_site+relativeLink+'?token='+str(new_user.pk)

            superusers = CustomUser.objects.filter(is_superuser=True)
           
            print(superusers)
            for email in superusers:
                email_body = 'Hi '+email.email+'\nA new user by the name '+new_user.email+' has been created, please click here to activate him \n'+absurl
                data = {'email_body':email_body, 'to_email':email.email, 'email_subject':'Verify your email'}
                Util.send_email(data)
            return Response({"Success":f"User {user} successfully created"}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors.values()},status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    serializer_class = ResetPasswordSerializer
    def post(self,request, format=None):
        try:
            user = CustomUser.objects.get(email=request.data.get('email'))
            if not user.is_active:
                return Response({"Error":"Sorry, your account has been deactivated"}, status=status.HTTP_401_UNAUTHORIZED)
            
        except:
            return Response({"Success":f"A reset link has been sent to your email if your email exists in our systems and is active"}, status=status.HTTP_200_OK)
        request.data['user'] = user.pk
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        request.data['token'] = token
        serializer = self.serializer_class(data=request.data)
        print(f'token is: {token}')
        if serializer.is_valid():
            AllToken = ResetPasswordModel.objects.filter(user=user) 
            for toke in AllToken: #Delete all previous tokens for that user
                toke.delete()
            serializer.save()
            current_site = get_current_site(request).domain
            relativeLink = reverse('reset-password-confirm')
            absurl = 'http://'+current_site+relativeLink+'?token='+token
            email_body = 'Hi '+user.email+'\nPlease click the link below to reset your password \n'+absurl
            data = {'email_body':email_body, 'to_email':user.email, 'email_subject':'Reset your password'}
            Util.send_email(data)
            return Response({"Success":f"A reset link has been sent to your email if your email exists in our systems and is active"}, status=status.HTTP_200_OK)
        return Response({"Success":f"A reset link has been sent to your email if your email exists in our systems and is active"}, status=status.HTTP_200_OK)
    
class ResetPasswordConfirm(APIView):
    serializer_class = ResetPasswordSerializer
    def get(self,request, format=None):
        try:
            token = request.GET.get('token')
            request.data['token'] = token
            print(token)
            user = ResetPasswordModel.objects.get(token=token)
            return Response({"Success":f"Please enter your new password"}, status=status.HTTP_200_OK)
        except:
            return Response({"Error":f"Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    def post(self,request, format=None):
        try:
            token = request.data['token'] 
            user = ResetPasswordModel.objects.get(token=token).user
        except:
            return Response({"Error":f"Token doesnt exist"}, status=status.HTTP_404_NOT_FOUND)
        request.data['created_at'] = ResetPasswordModel.objects.get(token=token).created_at
        request.data['user'] = user.pk
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(validated_data=request.data)
            return Response({"Success":f"Password reset successfully"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(email=request.data.get('email'))
            if not user.is_active:
                return Response({"Error":"Sorry, your account has been deactivated"}, status=status.HTTP_401_UNAUTHORIZED) 
            response = super().post(request, *args, **kwargs)
            return response
        except:
            return Response({"Error":"Wrong email or password"}, status=status.HTTP_401_UNAUTHORIZED)