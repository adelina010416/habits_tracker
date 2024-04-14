from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitOrAwardValidator, \
    TimeValidator, FrequencyValidator


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        validators = [HabitOrAwardValidator('connected_habit_id', 'award'),
                      TimeValidator('duration'),
                      FrequencyValidator('frequency')]
        exclude = ('user',)
