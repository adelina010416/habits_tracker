from rest_framework.permissions import BasePermission

from habits.models import Habit


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Habit):
            return obj.user == request.user
        return False
