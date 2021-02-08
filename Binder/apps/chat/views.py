from rest_framework import permissions
from rest_framework import viewsets, permissions
from .permissions import IsMessageOwner, IsChatOwner
from .serializers import ChatSerializer, MessageSerializer
from .models import Messages, Chat


# viewset for creating, retrieving and deleting chat by its owner on both sides
class ChatViewSet(viewsets.mixins.RetrieveModelMixin,
                viewsets.mixins.CreateModelMixin,
                viewsets.mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    permission_classes = (IsChatOwner, )
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# viewset for listing and creating messages
class MessageListCreateViewSet(viewsets.mixins.ListModelMixin,
                viewsets.mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  


# viewset for updating message by its owner
class MessageUpdatingViewSet(viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (IsMessageOwner, )
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)