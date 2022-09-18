import os

from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import home_application.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webrtc.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            home_application.routing.websocket_urlpatterns
        )
    ),

   
})