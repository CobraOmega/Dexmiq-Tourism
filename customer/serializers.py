from rest_framework import serializers
from .models import Customer
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model, authenticate
from rest_framework.validators import UniqueValidator

User = get_user_model()

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate_phone_number(self, value):
        """Ensure the phone number is valid."""
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Phone number must contain at least 10 digits.")
        return value
    
class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)  
    last_name = serializers.CharField(required=True)   
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already exists.")])
    phone_number = serializers.IntegerField(
        required=True,
        validators = [UniqueValidator(queryset = User.objects.all(), message = "Phone Number already exists.")])
    country = serializers.CharField(required = True)
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'phone_number', 'country', 'password', 'confirm_password',]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password:" "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password') #does not save confirm password

        # Username = first name + last name
        username = f"{validated_data['first_name']}{validated_data['last_name']}".lower()
        validated_data['username'] = username

        user = User.objects.create_user(**validated_data)
        return user

# Login
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user