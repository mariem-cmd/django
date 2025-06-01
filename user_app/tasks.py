from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_push_notification(email, message):
    print("✨✨✨ Début de la tâche send_push_notification ✨✨✨")
    print(f"📧 Destinataire : {email}")
    print("📨 Message à transmettre :")
    print(f"\"{message}\"")

    try:
        send_mail(
            subject="Notification Importante",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,  # à définir dans settings.py
            recipient_list=[email],
            fail_silently=False,
        )
        print("✅ Email envoyé avec succès ! 🎉")
        result = True
    except Exception as e:
        print(f"❌ Erreur lors de l’envoi de l’email : {e}")
        result = False

    print("✨✨✨ Fin de la tâche send_push_notification ✨✨✨")
    return result
 

from celery import shared_task
from user_app.models import ImageUpload
import cv2
import os
@shared_task
def process_image_ai(image_id):
    print("📸 Début du traitement AI de l'image...")

    try:
        image_obj = ImageUpload.objects.get(id=image_id)
        image_path = image_obj.image.path

        print(f"📂 Chargement de l'image depuis : {image_path}")
        img = cv2.imread(image_path)

        if img is None:
            raise ValueError("L'image est introuvable ou corrompue.")

        # Traitement AI simple : conversion en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        base, ext = os.path.splitext(image_path)
        processed_path = f"{base}_gray{ext}"
        cv2.imwrite(processed_path, gray)

        print(f"✅ Image traitée et sauvegardée à : {processed_path}")
        return {"status": "success", "path": processed_path}

    except Exception as e:
        print(f"❌ Erreur lors du traitement de l'image : {e}")
        return {"status": "error", "message": str(e)}