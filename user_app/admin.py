# user_app/admin.py
from django.contrib import admin
from .models import CustomUser

# Register the CustomUser model
admin.site.register(CustomUser)
