from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, exceptions
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import MyPagination
from habits.permission import IsOwner
from habits.serializer import HabitSerializer
from habits.services import validate_connected_habit


class HabitCreate(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.validated_data.get('connected_habit_id'):
            validate_connected_habit(
                serializer.validated_data['connected_habit_id'],
                self.request.user)
        serializer.save(user=self.request.user)


class MyHabitList(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_pleasant',)

    def get_queryset(self):
        user = self.request.user
        if user:
            return Habit.objects.filter(user=user)
        else:
            raise exceptions.PermissionDenied


class PublicHabitList(generics.ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_pleasant',)


class HabitRetrieve(generics.RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated & IsOwner]


class HabitUpdate(generics.UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated & IsOwner]

    def perform_update(self, serializer):
        if serializer.validated_data.get('connected_habit_id'):
            validate_connected_habit(serializer.
                                     validated_data['connected_habit_id'],
                                     self.request.user)
        serializer.save(user=self.request.user)


class HabitDestroy(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated & IsOwner]
