from django.urls import path
from .views import PayPalPaymentAPIView, PayPalExecuteView, paypal_webhook

urlpatterns = [
    path('payment/', PayPalPaymentAPIView.as_view(), name='paypal-payment'),
    path('execute/', PayPalExecuteView.as_view(), name='paypal-execute'),
    path('webhook/', paypal_webhook, name='paypal-webhook'),]
