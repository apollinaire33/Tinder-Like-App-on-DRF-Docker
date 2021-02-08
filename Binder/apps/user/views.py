from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from rest_framework import permissions
from .serializers import UserSerializer, UserListSerializer
from .services import adress_to_point, point_to_distance
from .permissions import IsOwner
User = get_user_model()


# view for creating user instance
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        name = data['name']
        email = data['email']
        password = data['password']

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'})
        else:
            if len(password) < 6:
                return Response({'error': 'Password must be at least 6 characters'})
            else:
                user = User.objects.create_user(email=email, password=password, name=name)

                user.save()
                return Response({'success': 'User created successfully'})


# viewset for dispaying list of users for everyone
class UserListViewSet(viewsets.mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserListSerializer

    def perform_create(self, serializer):  
        adress_to_point(self, serializer)

    def get_queryset(self):
        qs = super().get_queryset()
        return point_to_distance(self, qs)


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
        qs = super().get_queryset()
        user = super().get_object()
        qs1 = point_to_distance(self, qs)
        exact_user = [i for i in qs1 if i==user]
        return exact_user[0]

    def perform_update(self, serializer):
        adress_to_point(self, serializer)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# viewset for reading only user profile
class UserProfileViewSet(viewsets.mixins.RetrieveModelMixin,
                viewsets.mixins.UpdateModelMixin,
                viewsets.mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        qs = super().get_queryset()
        user = super().get_object()
        qs1 = point_to_distance(self, qs)
        exact_user = [i for i in qs1 if i==user]
        return exact_user[0]