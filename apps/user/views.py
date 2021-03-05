from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, viewsets, permissions
from rest_framework import permissions
from rest_framework import status

from user.serializers import UserSerializer, UserListSerializer, UserCreateSerializer
from user.services import GeoConverting as Geo
from user.services import UserValidation
from user.permissions import IsOwner

User = get_user_model()


# view for creating user instance
class SignupViewSet(viewsets.mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    

# viewset for dispaying list of users for everyone
class UserListViewSet(viewsets.mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserListSerializer

    def perform_create(self, serializer):  
        Geo.adress_to_point(self, serializer)

    def get_queryset(self):
        users_qs = super().get_queryset()
        return Geo.point_to_distance(self, users_qs)


# viewset for viewing and updating/deleting account by its owner
# viewset for liking users
class UserSelfProfileViewSet(viewsets.mixins.RetrieveModelMixin,
                viewsets.mixins.UpdateModelMixin,
                viewsets.mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    permission_classes = (IsOwner, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        users_qs = super().get_queryset()
        user = super().get_object()
        users_nearby_qs = Geo.point_to_distance(self, users_qs)
        exact_user = [i for i in users_nearby_qs if i==user]
        return exact_user[0]

    def perform_update(self, serializer):
        Geo.adress_to_point(self, serializer)


# viewset for reading only user profile
class UserProfileViewSet(viewsets.mixins.RetrieveModelMixin,
                viewsets.mixins.UpdateModelMixin,
                viewsets.mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        users_qs = super().get_queryset()
        user = super().get_object()
        users_nearby_qs = Geo.point_to_distance(self, users_qs)
        exact_user = [i for i in users_nearby_qs if i==user]
        return exact_user[0]