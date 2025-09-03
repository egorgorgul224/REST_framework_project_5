from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Класс описывает тесты для модели Habit."""

    def setUp(self):
        """Метод для создания первичных данных: пользователь, привычка, токен авторизации."""

        self.user = User.objects.create(email="admin@mail.ru")
        self.habit = Habit.objects.create(
            place="Test place", time="12:00", action="Action 1", reward="Test reward", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """Тест проверяет работу контроллера HabitCreateAPIView создания привычки. Проверяется корректный возврат
        статуса 201 и количество привычек в тестовой базе данных(2)."""

        url = reverse("habits:habit_create")
        data = {"place": "Test place №2", "time": "15:15", "action": "Action №2"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_create_with_nice_habit_error(self):
        """Тест проверяет работу контроллера HabitCreateAPIView создания привычки с некорректным вводом(признак
        приятной привычки с указанием связанной привычки и вознаграждения). Проверяется корректный возврат статуса 400
        и сообщение ошибки."""

        url = reverse("habits:habit_create")
        data = {
            "place": "Test place №2",
            "time": "15:15",
            "action": "Action №2",
            "is_nice_habit": True,
            "reward": "123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Для приятной привычки нельзя указать вознаграждение и связанную привычку.",
            response.data["non_field_errors"],
        )

    def test_habit_create_with_is_nice_related_habit_error(self):
        """Тест проверяет работу контроллера HabitCreateAPIView создания привычки с некорректным вводом(для полезной
        привычки можно выбрать только приятную привычку в поле related_habit). Проверяется корректный возврат статуса
        400 и сообщение ошибки."""

        url = reverse("habits:habit_create")
        data = {"place": "Test place №2", "time": "15:15", "action": "Action №2", "related_habit": self.habit.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Для полезной привычки можно выбрать только приятную привычку.", response.data["non_field_errors"]
        )

    def test_habit_create_with_related_reward_error(self):
        """Тест проверяет работу контроллера HabitCreateAPIView создания привычки с некорректным вводом(для полезной
        привычки можно указать только связанную привычку или вознаграждение). Проверяется корректный возврат статуса
        400 и сообщение ошибки."""

        self.nice_habit = Habit.objects.create(
            place="Test place", time="12:00", action="Action 1", is_nice_habit=True, owner=self.user
        )
        url = reverse("habits:habit_create")
        data = {
            "place": "Test place №2",
            "time": "15:15",
            "action": "Action №2",
            "related_habit": self.nice_habit.pk,
            "reward": "123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Для полезной привычки можно указать только связанную привычку или вознаграждение.",
            response.data["non_field_errors"],
        )

    def test_habit_retrieve(self):
        """Тест проверяет работу контроллера HabitRetrieveAPIView получения данных о привычке. Проверяется корректный
        возврат статуса 200 и места привычки."""

        url = reverse("habits:habit_detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), self.habit.place)

    def test_habit_update(self):
        """Тест проверяет работу контроллера HabitUpdateAPIView обновления данных о привычке. Проверяется корректный
        возврат статуса 200 и обновленное названия привычки."""

        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {
            "place": "New place",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), "New place")

    def test_habit_delete(self):
        """Тест проверяет работу контроллера HabitDestroyAPIView удаления привычки. Проверяется корректный возврат
        статуса 204 и количество привычек в базе данных(0)."""

        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self):
        """Тест проверяет работу контроллера HabitListAPIView вывода списка привычек. Проверяется корректный возврат
        статуса 200 и список привычек с пагинацией."""

        url = reverse("habits:habit_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "place": self.habit.place,
                    "time": "12:00:00",
                    "action": self.habit.action,
                    "related_habit": None,
                    "periodicity": self.habit.periodicity,
                    "reward": self.habit.reward,
                    "execute_time": self.habit.execute_time,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_published_list(self):
        """Тест проверяет работу контроллера HabitPublishedListAPIView вывода списка опубликованных привычек.
        Проверяется корректный возврат статуса 200 и список привычек с пагинацией."""

        url = reverse("habits:habit_published_list")
        response = self.client.get(url)
        data = response.json()
        result = {"count": 0, "next": None, "previous": None, "results": []}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
