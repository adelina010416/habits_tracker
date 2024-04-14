from collections import defaultdict
from datetime import datetime

from celery import shared_task

from habits.models import PlanHabit, Habit
from habits.services import telegram_check_updates, send_notification


@shared_task
def check_updates_and_send_reminder():
    telegram_check_updates()
    send_notification()


@shared_task
def get_plan_for_today():
    """Подготавливает список привычек, о которых нужно оповестить сегодня.
    Добавляет их в таблицу 'plan_habit'"""
    PlanHabit.objects.all().delete()  # удаляем все старые записи из таблицы
    today = datetime.today().date()  # получаем сегодняшнюю дату
    # получаем все полезные привычки
    all_habits = Habit.objects.filter(is_pleasant=False)
    # создаём словарь формата {frequency: [habit]}
    habits_by_frequency = defaultdict(list)
    plan_for_today = []  # список экземпляров привычки на сегодня
    for habit in all_habits:
        # {"1": [], "2": [], ...., "7": []}
        habits_by_frequency[habit.frequency].append(habit)
    # добавляем в план все ежедневные привычки
    plan_for_today += habits_by_frequency['1']
    del habits_by_frequency['1']
    for frequency, habits in habits_by_frequency.items():
        for habit in habits:
            # если привычка ещё ни разу не выполнялась, добавляем в план
            if not habit.last_execution:
                plan_for_today.append(habit)
            else:
                last_execution_date = habit.last_execution.date()
                date_difference = today - last_execution_date
                # если с последнего времени выполнения привычки
                # прошло указанное кол-во дней, добавляем в план
                if date_difference.days == habit.frequency:
                    plan_for_today.append(habit)
    for habit in plan_for_today:
        # добавляем привычки в БД
        PlanHabit.objects.create(today_habit=habit, time=habit.time)
