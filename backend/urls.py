from django.contrib import admin
from django.urls import path, include  # Corrigé : django.urls au lieu de django.utils
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt  # Corrigé : decorators
from user_app.schema import schema  # Assure-toi que schema.py existe bien
from user_app.views import  FeedView
urlpatterns = [
    path('admin/', admin.site.urls),  # Corrigé : pas d'apostrophe
    path('api/users/', include('user_app.urls')),
    path('api/users/graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
        # Corrigé : schema=schema
    path('feed/', FeedView.as_view()),
]