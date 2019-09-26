from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import scheduler_chat.routing
from scheduler_chat.custom_middlewares import (
    TokenAuthMiddlewareStack,
    QueryAuthUserMiddleware,
    QueryAuthTeamMiddleware
)
# channel_routing = {}

# How to do multiple authorizations from custom_middlewares?

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            scheduler_chat.routing.websocket_urlpatterns
        )
    ),
})

