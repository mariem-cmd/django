from celery import shared_task

@shared_task
def send_push_notification(user_id, message):
    print(f"Envoi notification à user {user_id} : {message}")
    # Ici tu pourrais intégrer un service réel (Firebase, APNS, etc.)
    return True
