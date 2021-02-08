from rest_framework import permissions


class IsChatOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.users


class IsMessageOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user