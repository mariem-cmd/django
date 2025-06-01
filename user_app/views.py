from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt

from .models import DeviceSession, ImageUpload
from .serializers import (
    UserSignupSerializer,
    UserSigninSerializer,
    DeviceSessionSerializer,
    ImageUploadSerializer,
)
from .tasks import process_image_ai  # ✅ Celery task import


# ✅ Crée un nouvel utilisateur
class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Utilisateur créé avec succès.", "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Authentifie l'utilisateur, génère tokens, crée/màj session appareil
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
                    "expiration_date": expires_at,
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
            {"error": "Identifiants invalides"}, status=status.HTTP_400_BAD_REQUEST
        )


# ✅ Vérifie que le token JWT est bien formé et valide
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


# ✅ Exemple de feed protégé
class FeedView(APIView):
    def get(self, request):
        data = [
            {"id": 1, "title": "Promo été", "image": "promo.jpg"},
            {"id": 2, "title": "Nouveaux produits", "image": "produit.jpg"},
        ]
        return Response(data)


# ✅ Upload image via fonction APIView + appel tâche Celery
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_image_view(request):
    serializer = ImageUploadSerializer(data=request.data)
    if serializer.is_valid():
        image = serializer.save(user=request.user)

        # ✅ Appel de la tâche Celery après sauvegarde
        process_image_ai.delay(image.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
