from django.urls import path
from .views import UserSignupView, UserSigninView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from .views import FeedView
from .views import upload_image_view

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', UserSigninView.as_view(), name='signin'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('feed/', FeedView.as_view()),
    path('upload-image/', upload_image_view, name='upload-image'),
] 

