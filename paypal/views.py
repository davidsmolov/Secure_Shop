from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from paypalrestsdk import Payment
import paypalrestsdk
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from store.models import Cart, CartItem
from store.serializers import CartReadSerializer, CartItemSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework.renderers import JSONRenderer
from .models import *
from .serializers import PayPalOrderSerializer

@permission_classes([IsAuthenticated])
class PayPalPaymentAPIView(APIView):
    def post(self, request, format=None):
        user = request.user
        try:
            cart = Cart.objects.filter(owner=user, completed=False)
            if cart.exists():
                cart = cart[0]
                cartitem = CartItem.objects.filter(cart=cart)
            else:
                return Response({"message": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"message": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)
        items = []
        for item in cartitem:
            items.append({
        "name": item.product.name,
        "price": str(item.product.price),
        "currency": "ILS",
        "quantity": item.quantity
    })
        try:
            payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://127.0.0.1/api/v1/paypal/execute/",
                "cancel_url": "http://127.0.0.1/api/v1/paypal/execute/"},
            "transactions": [{
                "item_list": {
                    "items":items},
                "amount": {
                    "total": str(cart.total),
                    "currency": "ILS"},
                "description": "This is the payment transaction description."}]})

            if payment.create():
            # Redirect user to this URL for PayPal payment
                payment_id=payment['id']
                paypal_order = PayPalOrder.objects.create(payment_id=payment_id, user=user, cart=cart)
                paypal_order.save()
                return Response({"payment_url": payment.links[1].href})
            else:
                return Response({"fail":f"{payment.error}"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PayPalExecuteView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            payment_id = request.GET.get('paymentId')
            payer_id = request.GET.get('PayerID')
        

            payment = Payment.find(payment_id)
            
        except paypalrestsdk.exceptions.ResourceNotFound:
            return Response({"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
            

        if payment.execute({"payer_id": payer_id}):
            # Payment executed successfully
            return Response({"message": "Payment executed successfully"}, status=status.HTTP_200_OK)
        else:
            # Payment execution failed
            return Response(payment.error, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def paypal_webhook(request):

    if request.method == "POST":
        # Parse the webhook notification
        webhook_notification = json.loads(request.body.decode('utf-8'))
        # Check if the event is a payment capture completed event
        if webhook_notification["event_type"] == "PAYMENTS.PAYMENT.CREATED" or webhook_notification["event_type"] == "PAYMENTS.PAYMENT.CAPTURE.COMPLETED":
            # Get the payment ID from the webhook notification
            payment_id = webhook_notification["resource"]["id"]
            # Get the payment details from PayPal
            paypalorder = PayPalOrder.objects.get(payment_id=payment_id)
            if paypalorder.cart.completed == True:
                return HttpResponse(status=200)
            paypalorder.approved = True
            paypalorder.save()
            cart = paypalorder.cart
            cart.completed = True
            cart.save()
            cartitem = CartItem.objects.filter(cart=cart)
            for carti in cartitem:
                product = carti.product
                product.stock -= carti.quantity
                product.save()
                
            
            payment = paypalrestsdk.Payment.find(payment_id)
            
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)