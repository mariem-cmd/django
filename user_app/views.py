from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer, UserSigninSerializer, DeviceSessionSerializer
from .models import DeviceSession
from django.utils import timezone
from datetime import timedelta
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response

# ✅ Crée un nouvel utilisateur
class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "Utilisateur créé avec succès.",
                    "user": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Authentifie l'utilisateur, génère token, crée/màj session appareil point 1
class UserSigninView(APIView):
    def post(self, request):
        serializer = UserSigninSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            device_id = request.data.get("device_id")
            if not device_id:
                return Response(
                    {"error": "Device ID is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            expires_at = timezone.now() + timedelta(days=7)

            session, created = DeviceSession.objects.update_or_create(
                user=user,
                device_id=device_id,
                defaults={
                    "token": access_token,
                    "expiration_date": expires_at,  # ✅ Corrected
                    "device_info": request.data.get("device_info", "Unknown device"),
                },
            )

            return Response(
                {
                    "message": "Connexion réussie.",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "session": DeviceSessionSerializer(session).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Identifiants invalides"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ✅ Vérifie que le token JWT est bien formé et valide po,t 2
def validate_jwt_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
        return payload
    except ExpiredSignatureError:
        return {"error": "Token expiré"}
    except InvalidTokenError:
        return {"error": "Token invalide"}
    
class FeedView(APIView):
    def get(self, request):
        data = [
            {"id": 1, "title": "Promo été", "image": "promo.jpg"},
            {"id": 2, "title": "Nouveaux produits", "image": "produit.jpg"},
        ]
        return Response(data)

