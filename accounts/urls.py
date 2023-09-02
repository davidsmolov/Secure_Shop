from django.contrib import admin
from django.urls import path, include
from .views import *
from accounts.views import UserRegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('reset-password-confirm/', ResetPasswordConfirm.as_view(), name='reset-password-confirm'),
]
