from apps.user.views import SignupViewSet
from django.urls import path
from rest_framework import routers

from user.views import SignupViewSet, UserListViewSet, UserSelfProfileViewSet, UserProfileViewSet


router = routers.DefaultRouter()
router.register(r'', UserListViewSet)
router.register(r'update_account', UserSelfProfileViewSet)
router.register(r'view_account', UserProfileViewSet)
router.register(r'signup', SignupViewSet)

urlpatterns = [
]

urlpatterns += router.urls