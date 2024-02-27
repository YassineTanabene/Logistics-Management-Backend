# accounts/serializers.py
import statistics
from rest_framework import serializers
from .models import Camion, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email cannot be empty")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password cannot be empty")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        # Check for duplicate email
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})

        user = CustomUser(email=email)
        user.set_password(password)
        user.save()
        return user

class CamionSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Camion
        fields = '__all__'
        read_only_fields = ['id']
