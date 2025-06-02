🧾 Document Explicatif – Projet Django + Flutter

1. ⚙️ Installation des dépendances
✅ Ce que j’ai fait
Liste des dépendances dans requirements.txt.

Étapes :
bash
pip install -r requirements.txt


2. 🧍 Modèles Django : CustomUser et DeviceSession

✅ Ce que j’ai fait
Défini deux modèles :
CustomUser (utilisateur personnalisé)
DeviceSession (suivi des connexions par appareil)

Étapes :
bash
python manage.py makemigrations
python manage.py migrate

⚙️ Tester avec Postman :
Créer un compte
URL : POST http://127.0.0.1:8000/api/users/signup/
Body (JSON) :
{
  "full_name": "name",
  "email": "email1@example.com",
  "password": "Motdepasse12"
}
Se connecter (crée une session device)

URL : POST http://127.0.0.1:8000/api/users/signin/
Body :
{
  "email": "email1@example.com",
  "password": "Motdepasse12",
  "device_id": "flutter_device_004"
}
✅ Une session DeviceSession est automatiquement créée.


3. ⏳ Expiration de session et validation JWT

✅ Ce que j’ai fait
Ajout de is_expired() dans DeviceSession
Vérification JWT avec PyJWT

⚙️Test :
Envoyer un token valide dans les headers → accepte.
Attendre expiration → rejet avec 401.


4. 📦 Serializers DRF + GraphQL Types

✅ Ce que j’ai fait
CustomUserSerializer, DeviceSessionSerializer
Types GraphQL : AppUserType, DeviceSessionType

Fichiers :
serializers.py
types.py

⚙️ Tester avec Postman :
URL : POST http://127.0.0.1:8000/api/users/graphql/
Headers :
Authorization: JWT <votre_token>
Content-Type: application/json
Exemples de requêtes :
{ "query": "{ allUsers { id fullName email } }" }
{ "query": "query { me { fullName email } }" }
{ "query": "{ mySessions { id deviceId deviceInfo isExpired } }" }

5. 🌐 Endpoints REST
✅ Ce que j’ai fait
Création de :
POST /signup/
POST /signin/
GET /feed/

⚙️Test :
Authentifie-toi via /signin/, récupère le token.

Utilise ce token pour appeler :
{ "query": "{ feed { id title image } }" }


6. 🧬 Requêtes & Mutations GraphQL

✅ Ce que j’ai fait
Mutation likeItem dans schema.py
Exemple :
{ "query": "mutation { likeItem(itemId: 1) { success } }" }



7. 🔒 Sécurisation : JWT, HTTPS, Validation

✅ Ce que j’ai fait
Authentification avec JWT (via djangorestframework-simplejwt)
Validation des champs dans serializers.py
Préparation du projet pour HTTPS

⚙️Tester :
Essayer d’accéder à un endpoint GraphQL sans token → rejet (401)
Tester /signup/ avec des champs invalides → 400


8. 📬 Tâches Celery : Notifications & Synchronisation

✅ Ce que j’ai fait
Tâche send_push_notifications() avec  Gmail
Tâche sync_offline_data() pour la sync périodique

Configuration :
Redis installé et lancé

Lancer Celery :
bash
celery -A backend worker --loglevel=info -P solo

⚙️Tester :
Ouvrir shell Django :

bash
python manage.py shell
Appeler :
from user_app.tasks import send_push_notifications
send_push_notifications.delay()
✅ L’email (ou log) est envoyé si config correcte.


🔐 Étapes pour générer un mot de passe d’application Gmail (pour Django)
✅ Pré-requis
Tu dois :
•	Avoir activé la vérification en 2 étapes sur ton compte Gmail.
•	Utiliser une adresse Gmail .
________________________________________
🧭 Étapes détaillées :
1.	Connecte-toi à ton compte Google
➡️ Va sur : https://myaccount.google.com
2.	Clique sur “Sécurité” dans le menu à gauche
3.	Active la vérification en deux étapes (si ce n’est pas déjà fait)
➡️ Clique sur “Validation en deux étapes”
➡️ Suis les étapes : tu vas devoir confirmer avec ton téléphone.
4.	Retourne à la page “Sécurité”
5.	En bas, clique sur “Mots de passe des applications”
📌 Lien direct : https://myaccount.google.com/apppasswords 
6.	Connexion à nouveau si demandé
7.	Créer un mot de passe d’application :
o	Dans Sélectionner l'application, choisis : Mail
o	Dans Sélectionner l’appareil, choisis : Autre (personnalisé) et écris : Django
o	Clique sur Générer
8.	✅ Google affiche un mot de passe spécial comme :
 
9.	🔐 Ce mot de passe, tu dois le copier et le coller dans ton fichier settings.py :
 
10. ✉️ Modifier l’adresse email utilisée dans Django settings.py pour l’envoi de mails





9. 🖼️ Traitement d’image avec IA (OpenCV)
✅ Ce que j’ai fait
Tâche Celery process_image_ai
Transforme l’image en niveaux de gris avec OpenCV

Étapes de test :
Lancer Redis & Celery

bash
celery -A backend worker --loglevel=info -P solo
Envoyer une image via Postman :

URL : POST http://127.0.0.1:8000/api/users/upload-image/

Body : form-data avec image

✅ Une image _gray.jpg est enregistrée automatiquement