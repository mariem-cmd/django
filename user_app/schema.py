import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from user_app.types import AppUserType, DeviceSessionType
from .models import DeviceSession
from django.contrib.auth import get_user_model

User = get_user_model()

# ---------------- TYPES POUR LE FEED ----------------
class FeedType(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    image = graphene.String()

# ---------------- QUERIES ----------------
class Query(graphene.ObjectType):
    # Pour l'utilisateur connecté
    me = graphene.Field(AppUserType)
    my_sessions = graphene.List(DeviceSessionType)
    all_users = graphene.List(AppUserType)

    @login_required
    def resolve_me(self, info):
        return info.context.user

    @login_required
    def resolve_my_sessions(self, info):
        return DeviceSession.objects.filter(user=info.context.user)

    def resolve_all_users(self, info):
        return User.objects.all()

    # Le "feed" simulé
    feed = graphene.List(FeedType)

    def resolve_feed(self, info):
        return [
            {"id": 1, "title": "Promo été", "image": "promo.jpg"},
            {"id": 2, "title": "Nouveaux produits", "image": "produit.jpg"},
        ]

# ---------------- MUTATIONS ----------------
class LikeItem(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        item_id = graphene.Int()

    def mutate(self, info, item_id):
        user = info.context.user
        if user.is_authenticated:
            print(f"{user.email} a liké l’article {item_id}")
            return LikeItem(success=True)
        return LikeItem(success=False)

class Mutation(graphene.ObjectType):
    like_item = LikeItem.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# ---------------- SCHÉMA FINAL ----------------
schema = graphene.Schema(query=Query, mutation=Mutation)
