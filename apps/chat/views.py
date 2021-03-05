from rest_framework import permissions
from rest_framework import viewsets, permissions

from chat.permissions import IsMessageOwner, IsChatOwner
from chat.serializers import ChatSerializer, MessageSerializer
from chat.models import Message, Chat


# viewset for creating, retrieving and deleting chat by its owner on both sides
class ChatViewSet(viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.CreateModelMixin,
                    viewsets.mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (IsChatOwner, )
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


# viewset for listing and creating messages
class MessageListCreateViewSet(viewsets.mixins.ListModelMixin,
                    viewsets.mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


# viewset for updating message by its owner
class MessageUpdatingViewSet(viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (IsMessageOwner, )
    queryset = Message.objects.all()
    serializer_class = MessageSerializer