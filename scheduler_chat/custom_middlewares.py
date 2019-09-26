
import jwt
from django.db import close_old_connections
from scheduler_teams.models import CustomTeam
from scheduler_app.models import CustomUser
from django.core import exceptions
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser

class QueryAuthUserMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()
        user_id = CustomUser.objects.get(id=int(scope["query_string"])).id
        scope['user_id'] = user_id
        return self.inner(scope)


class QueryAuthTeamMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()
        try:
            team = CustomTeam.objects.get(id=int(scope["query_string"])).id
            scope['team_id'] = team
        except exceptions.ObjectDoesNotExist:
            return "Object does not exist"

        return self.inner(scope)


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def get_id_from_token(self, token):
        user = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
        user_id = user['user_id']
        return user_id 

    def __call__(self, scope):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token = headers['HTTP_AUTHORIZATION']
            # token = headers['authorization']
            user_id = self.get_id_from_token(token)
            scope['user'] = token.user

        return self.inner(scope)


QueryAuthMiddlewareStack = lambda inner: QueryAuthUserMiddleware(AuthMiddlewareStack(inner))
TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
