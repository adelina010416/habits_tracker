from django.forms import model_to_dict
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, PlanHabit
from habits.tasks import get_plan_for_today
from users.models import User

correct_data = {
    "action": "test_create",
    "time": "23:09:00",
    "place": "где-угодно",
    "frequency": "3",
    "duration": "00:01:00"
}
data_invalid_award = {
    "action": "test_create_pleasant",
    "time": "23:09:00",
    "place": "где-угодно",
    "frequency": "3",
    "duration": "00:01:00",
    "is_pleasant": True,
    "award": 'award'
}
data_invalid_frequency = {
    "action": "test_create_frequency",
    "time": "23:09:00",
    "place": "где-угодно",
    "frequency": "99",
    "duration": "00:01:00",
    "award": 'award'
}


class HabitsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@mail.ru', is_active=True, is_staff=False)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.pleasant_habit = Habit.objects.create(
            action='test_pleasant_action',
            time='22:00:00',
            place='test_place',
            frequency='1',
            duration='00:01:00',
            user=self.user,
            is_public=True)
        self.useful_public_habit = Habit.objects.create(
            action='test_useful_action_public',
            time='22:00:00',
            place='test_place',
            frequency='2',
            duration='00:01:00',
            connected_habit_id=self.pleasant_habit.id,
            user=self.user,
            is_public=True)
        self.useful_private_habit = Habit.objects.create(
            action='test_useful_action_private',
            time='22:00:00',
            place='test_place',
            frequency='3',
            duration='00:01:00',
            award='test_award',
            user=self.user)
        self.user_another = User.objects.create(email='test2@mail.ru',
                                                is_active=True,
                                                is_staff=False)
        self.user_another.set_password('test_password')
        self.user_another.save()

    def test_habit_list(self):
        """ Проверка списка публичных привычек """
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [model_to_dict(self.pleasant_habit, exclude=['user']),
                          model_to_dict(self.useful_public_habit,
                                        exclude=['user'])])

    def test_my_habit_list(self):
        """ Проверка списка личных привычек """
        response = self.client.get('/my-habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             "count": 3,
                             "next": None,
                             "previous": None,
                             "results":
                                 [model_to_dict(self.pleasant_habit,
                                                exclude=['user']),
                                  model_to_dict(self.useful_public_habit,
                                                exclude=['user']),
                                  model_to_dict(self.useful_private_habit,
                                                exclude=['user'])]
                         }
                         )

    def test_habit_retrieve(self):
        """ Проверка получения привычки """
        response = self.client.get(f'/{self.useful_private_habit.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         model_to_dict(self.useful_private_habit,
                                       exclude=['user'])
                         )
        self.client.force_authenticate(user=self.user_another)
        response = self.client.get(f'/{self.useful_private_habit.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(),
                         {'detail': 'You do not have permission '
                                    'to perform this action.'}
                         )

    def test_habit_create(self):
        """ Проверка создания привычки """
        valid_response = self.client.post('/create/', data=correct_data)
        invalid_award_response = self.client.post('/create/',
                                                  data=data_invalid_award)
        invalid_frequency_response = self.client.post(
            '/create/', data=data_invalid_frequency)
        self.assertEqual(valid_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(invalid_award_response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(invalid_frequency_response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(invalid_award_response.json(),
                         {"non_field_errors":
                             [
                                 "Приятная привычка не может иметь "
                                 "вознаграждение!"
                             ]})

    def test_habit_update(self):
        """ Проверка обновления привычек """
        response = self.client.patch(
            f'/update/{self.useful_public_habit.id}',
            data=correct_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        """ Проверка удаления привычки """
        delete_habit = Habit.objects.create(action='test_delete',
                                            time='22:00:00',
                                            place='test_place',
                                            frequency='1',
                                            duration='00:01:00',
                                            user=self.user,
                                            is_public=True)
        response = self.client.delete(f'/delete/{delete_habit.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TasksAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru')
        self.habit1 = Habit.objects.create(action='test1',
                                           time='22:00:00',
                                           place='test_place',
                                           frequency='1',
                                           duration='00:01:00',
                                           user=self.user,
                                           is_public=True)
        self.habit2 = Habit.objects.create(action='test2',
                                           time='22:00:00',
                                           place='test_place',
                                           frequency='7',
                                           duration='00:01:00',
                                           user=self.user,
                                           is_public=True,
                                           last_execution='2024-04-13'
                                                          ' 22:56:07')

    def test_get_plan_for_today(self):
        self.assertEqual(PlanHabit.objects.all().count(), 0)
        get_plan_for_today()
