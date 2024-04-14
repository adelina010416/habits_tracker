from django.db import models

from constants import nullable
from users.models import User


class Habit(models.Model):
    FREQUENCY_CHOICES = (
        ('1', 'ежедневно'),
        ('2', 'раз в два дня'),
        ('3', 'раз в три дня'),
        ('4', 'раз в четыре дня'),
        ('5', 'раз в пять дней'),
        ('6', 'раз в шесть дней'),
        ('7', 'раз в семь дней'),
    )
    action = models.CharField(max_length=250, verbose_name='действие')
    time = models.TimeField(verbose_name='время')
    place = models.CharField(max_length=250, verbose_name='место')
    frequency = models.CharField(max_length=20,
                                 default='1',
                                 choices=FREQUENCY_CHOICES,
                                 verbose_name='периодичность')
    duration = models.TimeField(verbose_name='время на выполнение')
    user = models.ForeignKey(User,
                             **nullable,
                             on_delete=models.CASCADE,
                             verbose_name='пользователь')
    # признак приятной привычки (по умолчанию False - полезная)
    is_pleasant = models.BooleanField(
        default=False, verbose_name='признак приятной привычки')
    # приятная привычка (используется как альтернатива вознаграждению)
    connected_habit_id = models.PositiveIntegerField(
        **nullable, verbose_name='связанная привычка')
    # чем пользователь должен себя вознаградить после выполнения
    # (указывается только если не указана connected_habit)
    award = models.CharField(
        max_length=250, **nullable, verbose_name='вознаграждение')
    # могут ли другие пользователи брать в пример эту привычку
    is_public = models.BooleanField(
        default=False, verbose_name='признак публичности')
    # когда привычку выполняли в последний раз
    last_execution = models.DateTimeField(
        default=None, **nullable, verbose_name='последнее выполнение')

    def __str__(self):
        return f"Привычка {self.action}"

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'


class PlanHabit(models.Model):
    today_habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, verbose_name='сегодняшняя привычка')
    time = models.TimeField(verbose_name='время')

    def __str__(self):
        return f"{self.today_habit}, запланированная на сегодня в {self.time}"

    class Meta:
        verbose_name = 'Привычка на сегодня'
        verbose_name_plural = 'Привычки на сегодня'
