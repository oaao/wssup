from channels.auth    import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

application = ProtocolTypeRouter(
    {
        # 'http': channels.http.AsgiHandler (django views) added by default
        'websocket': AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
    }
)
