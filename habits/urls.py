from django.urls import path

from habits.apps import HabitsConfig
from habits.views import MyHabitList, PublicHabitList, HabitRetrieve, \
    HabitCreate, HabitUpdate, HabitDestroy

app_name = HabitsConfig.name

urlpatterns = [
    path('my-habits/', MyHabitList.as_view(), name='my_habits_list'),
    path('', PublicHabitList.as_view(), name='habits_list'),
    path('<int:pk>', HabitRetrieve.as_view(), name='habit'),
    path('create/', HabitCreate.as_view(), name='create_habit'),
    path('update/<int:pk>', HabitUpdate.as_view(), name='update_habit'),
    path('delete/<int:pk>', HabitDestroy.as_view(), name='delete_habit'),
]
