import jwt
from django.http import JsonResponse
from shop.settings import SECRET_KEY as secret_key
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


def extract_info_from_jwt(request):
    # Get the JWT token from the request (e.g., from headers, query parameters, etc.)
    jwt_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]

    # Replace 'your_secret_key' with the actual secret key used to sign the JWT token.
    # Ensure it's the same key used to create the JWT in the first place.

    try:
        # Decode the JWT token and get the payload (claims)
        payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])

        # The payload variable now contains the extracted information from the JWT
        # You can access specific information using the keys in the payload dictionary
        email = payload.get('email')
        # Process the extracted information as needed
        # ...
        return email
    except jwt.ExpiredSignatureError:
        # Handle token expiration
        return Response({'error': 'Token has expired.'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        # Handle invalid tokens
        return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)


    return response

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except AuthenticationFailed as ex:
            raise AuthenticationFailed({"Error":"Problem with the jwt"})