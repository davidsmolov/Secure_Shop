from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, ResetPassword
import re
import datetime
from django.utils import timezone
from django.contrib.auth.hashers import check_password





                
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add password field manually
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')


    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError({"Error":"Password has to be at least 8 characters"})
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError({"Error": "Password must contain at least one capital letter"})

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError({"Error": "Password must contain at least one number"})

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError({"Error": "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"})
        return make_password(password)
        

    def validate_first_name(self, first_name):
        pattern= r"^[a-zA-Z]+$"
        if not re.match(pattern, first_name):
            raise serializers.ValidationError({"Error":"First name can be letters only"})
        return first_name

    def validate_last_name(self, last_name):
        pattern= r"^[a-zA-Z]+$"
        if not re.match(pattern, last_name):
            raise serializers.ValidationError({"Error":"Last name can be letters only"})
        return last_name

           
    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        return user

class ResetPasswordSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(default=timezone.now)
    class Meta:
        model = ResetPassword
        fields = ('user', 'token', 'created_at')

class SetNewPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    user = serializers.CharField(max_length=555)
    new_password = serializers.CharField(min_length=8, write_only=True)
    created_at = serializers.DateTimeField()
    
    class Meta:
        model = ResetPassword
        fields = ('token', 'user', 'new_password', 'created_at')
        
    def get_new_password(self, validated_data):
        return validated_data.get('new_password', None)
    
    def validate_created_at(self, created_at):
        print(created_at)
        if created_at + datetime.timedelta(minutes=15) < timezone.now():
            raise serializers.ValidationError({"Error": "Token expired"})
    def validate_new_password(self, new_password):
        user = CustomUser.objects.get(pk=self.initial_data['user'])
        if check_password(new_password, user.password):
            raise serializers.ValidationError({"Error": "New password cannot be the same as the old password"})          
        if len(new_password) < 8:
            raise serializers.ValidationError({"Error":"Password has to be at least 8 characters"})
        if not any(char.isupper() for char in new_password):
            raise serializers.ValidationError({"Error": "Password must contain at least one capital letter"})

        if not any(char.isdigit() for char in new_password):
            raise serializers.ValidationError({"Error": "Password must contain at least one number"})

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
            raise serializers.ValidationError({"Error": "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"})
        return make_password(new_password)
    
    def save(self, validated_data):
        new_password = validated_data.pop('new_password')
        user = CustomUser.objects.get(pk=validated_data.pop('user'))
        user.password = make_password(new_password)
        user.save()
        ResetPasswordInstance = ResetPassword.objects.get(token=validated_data.pop('token'))
        ResetPasswordInstance.delete()
        return user
    
        
        
        