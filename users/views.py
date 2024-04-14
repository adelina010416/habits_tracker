from datetime import datetime

import pytz
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from config.settings import TIME_ZONE
from users.models import User
from users.permissions import IsOwner
from users.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.data['password'])
        user.save()


class UserAuth(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data.get('email')).first()
        user.last_login = datetime.now(pytz.timezone(TIME_ZONE))
        user.save()
        return super().post(request, *args, **kwargs)
