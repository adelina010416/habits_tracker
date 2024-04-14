import json
import time

import requests
from rest_framework import serializers

from config import settings
from habits.models import Habit, PlanHabit
from users.models import User


def validate_connected_habit(connected_habit_id, user):
    if not Habit.objects.filter(user=user, id=connected_habit_id).exists():
        raise serializers.ValidationError(
            'Связанная привычка не найдена. '
            'Пожалуйста, выберите существующую привычку '
            'или добавьте новую и укажите её в качестве связанной.')


def send_message(t_username, message):
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage'
    requests.post(
        url=url,
        data={
            "chat_id": t_username,
            "text": message
        }
    )


def open_last_update_file():
    """Считывает или при необходимости создаёт файл 'last_update.json',
    в котором хранится ID последнего проверенного обновления.
    :return last_update:int"""
    try:
        with open('last_update.json') as file:
            last_update = json.load(file)['last_update']
    except FileNotFoundError:
        with open('last_update.json', 'w') as file:
            file.write(json.dumps({"last_update": 0}))
            last_update = 0
    return last_update


def write_down_last_update(update_id):
    """Принимает и записывает в файл новое значение последнего
    проверенного обновления.
    :arg update_id:int"""
    with open('last_update.json', 'w') as file:
        file.write(json.dumps({"last_update": update_id}))


def telegram_check_updates():
    # считываем из файла ID последнего обновления
    last_update = open_last_update_file()
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}" \
          f"/getUpdates?offset={last_update + 1}"
    response = requests.post(url=url, data={"allowed_updates": ["message"]})

    if response.status_code == 200:
        # перезаписываем в файл ID последнего обновления
        try:
            last_update_id = response.json()["result"][-1]['update_id']
        except IndexError:
            last_update_id = 0
        write_down_last_update(last_update_id)
        for telegram_update in response.json()["result"]:
            if telegram_update.get('message'):
                telegram_user_chat_id = \
                    telegram_update["message"]["from"]["id"]
                telegram_user_name = \
                    telegram_update["message"]["from"]["username"]
                user = User.objects.filter(
                    telegram_username=f'@{telegram_user_name}')
                if user.exists():
                    # если юзер есть в БД, проверяем наличие его телеграм id
                    # у нас в БД
                    # если его нет, записываем, сохраняем
                    if user.first().telegram_user_id is None:
                        user.telegram_user_id = telegram_user_chat_id
                        user.save()
                    send_message(
                        telegram_user_chat_id,
                        f'Привет, '
                        f'{telegram_update["message"]["from"]["first_name"]}! '
                        f'Бот успешно активирован!')
                else:
                    # если пользователя нет в БД,
                    # отправляем приглашение снача зарегистрироваться на сайте
                    send_message(
                        telegram_user_chat_id,
                        'Для использования уведомлений чат-бота сначала '
                        'зарегистрируйтесь на нашем сайте')


def send_notification():
    time_now = time.strftime("%H:%M", time.localtime())
    habits_for_now = PlanHabit.objects.filter(time=time_now)
    for habit in habits_for_now:
        if habit.today_habit.award:
            key_word = 'получить'
            award = habit.today_habit.award
        elif habit.today_habit.connected_habit_id:
            key_word = ''
            award = Habit.objects.filter(
                id=habit.today_habit.connected_habit_id).first().action
        else:
            award = ''
            key_word = 'отдохнуть и создать на будущее для себя ' \
                       'вознаграждение' \
                       ' за выполнение этой полезной привычки ;)'
        message = f'Время для того, чтобы "{habit.today_habit.action}" в ' \
                  f'"{habit.today_habit.place}".\n' \
                  f'А после сможете {key_word} {award}'
        send_message(habit.today_habit.user.telegram_user_id, message)
