from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import DeviceSession
from django.contrib.auth import get_user_model
from .models import ImageUpload



# Custom User Signup Serializer
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()  # This will use your CustomUser model
        fields = ['full_name', 'email', 'password']

    def create(self, validated_data):
        # Creating the user using the CustomUser model
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
        )
        return user


# Custom User Signin Serializer
class UserSigninSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        # Fetch the custom user model
        user = get_user_model().objects.filter(email=data['email']).first()
        if user and user.check_password(data['password']):
            return user  # Return user if credentials match
        raise serializers.ValidationError("Invalid email or password")
    

class DeviceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSession
        fields = ['id', 'user', 'device_id', 'token', 'created_at', 'expiration_date']   


# Ajouter un serializer pour retourner les données de l’utilisateur connecté
User = get_user_model()

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'date_joined']



class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload  # ton modèle
        fields = ['id', 'image', 'user']
        read_only_fields = ['user']

