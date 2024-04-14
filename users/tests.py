from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

correct_data = {
    "password": "test123test456",
    "email": "testcreate@mail.ru",
    "telegram_username": "@test"
}


class HabitsAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@mail.ru', is_active=True, is_staff=False)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.user1 = User.objects.create(
            email='testdelete@mail.ru', is_active=True, is_staff=False)
        self.user1.set_password('test_password')
        self.user1.save()

    def test_user_list(self):
        """ Проверка списка пользователей"""
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_user_retrieve(self):
        """ Проверка пользователя """
        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        """ Проверка создания пользователя """
        response = self.client.post('/users/', data=correct_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_update(self):
        """ Проверка обновления пользователя """
        response = self.client.patch(
            f'/users/{self.user.id}/', data=correct_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #

    def test_user_delete(self):
        """ Проверка удаления пользователя """
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/users/{self.user1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
