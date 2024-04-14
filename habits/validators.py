from datetime import datetime

from rest_framework import serializers

from habits.models import Habit


class HabitOrAwardValidator:
    def __init__(self, habit, award):
        self.habit = habit
        self.award = award

    def __call__(self, value):
        connected_habit_id = value.get(self.habit)
        if connected_habit_id:
            habit = Habit.objects.filter(id=connected_habit_id)
            # если привычка полезная
            if not value.get('is_pleasant'):
                connected_habit_id = value.get(self.habit)
                award_str = value.get(self.award)
                # исключает одновременный выбор связанной привычки
                # и указания вознаграждения.
                if connected_habit_id and award_str:
                    raise serializers.ValidationError(
                        'Выберите что-либо одно: либо приятную '
                        'привычку, либо вознаграждение.')
                # В связанные привычки могут попадать только привычки
                # с признаком приятной привычки.
                if habit.exists() and not habit.first().is_pleasant:
                    raise serializers.ValidationError(
                        'Связанная привычка должна быть приятной!')
            else:
                # У приятной привычки не может быть связанной привычки.
                if value.get(self.habit):
                    raise serializers.ValidationError(
                        'Приятная привычка не может иметь связанную привычку!')
        # У приятной привычки не может быть вознаграждения.
        if value.get('is_pleasant') and value.get(self.award):
            raise serializers.ValidationError(
                'Приятная привычка не может иметь вознаграждение!')


class TimeValidator:
    def __init__(self, duration):
        self.duration = duration

    def __call__(self, value):
        if value.get('duration'):
            limit = datetime.strptime('02:00:00', "%H:%M:%S").time()
            if value.get('duration') > limit:
                raise serializers.ValidationError(
                    'Время выполнения привычки не должно превышать 2 часов.')


class FrequencyValidator:
    def __init__(self, frequency):
        self.frequency = frequency
        self.frequency_list = ['1', '2', '3', '4', '5', '6', '7']

    def __call__(self, value):
        if value.get(self.frequency):
            if value.get(self.frequency) not in self.frequency_list:
                raise serializers.ValidationError(
                    'Нельзя выполнять привычку реже, чем раз в неделю.')
