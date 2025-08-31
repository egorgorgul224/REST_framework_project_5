from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Класс описывает тесты для модели User."""

    def setUp(self):
        """Метод для создания первичных данных: пользователь, токен авторизации."""

        self.user = User.objects.create(email="admin@mail.ru")
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """Тест проверяет работу контроллера UserCreateAPIView регистрации пользователя. Проверяется корректный возврат
        статуса 201 и количество пользователей в тестовой базе данных(2)."""

        url = reverse("users:register")
        data = {"email": "user1@mail.ru", "password": "qwert12345"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_retrieve(self):
        """Тест проверяет работу контроллера UserRetrieveAPIView получения данных о пользователе. Проверяется
        корректный возврат статуса 200 и почту пользователя."""

        url = reverse("users:user_detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_update(self):
        """Тест проверяет работу контроллера UserUpdateAPIView обновления данных о пользователе. Проверяется корректный
        возврат статуса 200 и обновленное имя пользователя."""

        url = reverse("users:user_update", args=(self.user.pk,))
        data = {
            "first_name": "Ivan",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("first_name"), "Ivan")

    def test_user_delete(self):
        """Тест проверяет работу контроллера UserDestroyAPIView удаления пользователя. Проверяется корректный возврат
        статуса 204 и количество ползователей в базе данных(0)."""

        url = reverse("users:user_delete", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
