from django.urls import path
from rest_framework import routers
from .views import SignupView, UserListViewSet, UserSelfProfileViewSet, UserProfileViewSet


router = routers.DefaultRouter()
router.register(r'', UserListViewSet)
router.register(r'update_account', UserSelfProfileViewSet)
router.register(r'view_account', UserProfileViewSet)

urlpatterns = [
    path('signup', SignupView.as_view()),
]

urlpatterns += router.urls