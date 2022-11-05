from rest_framework import permissions

from ads.models import User


class IsOwnerOrStuff(permissions.BasePermission):
    message = 'У вас нет прав на редактирование подборок.'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return False


class IsOwnerOrStuffAd(permissions.BasePermission):
    message = 'У вас нет прав на редактирование объявлений.'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.role in [User.MODERATOR, User.ADMIN]:
            return True
        return False
