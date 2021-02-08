from rest_framework import routers
from .views import ChatViewSet, MessageListCreateViewSet, MessageUpdatingViewSet


router = routers.DefaultRouter()

router.register(r'chat', ChatViewSet)
router.register(r'messages', MessageListCreateViewSet)
router.register(r'messages/update_message', MessageUpdatingViewSet)

urlpatterns = router.urls