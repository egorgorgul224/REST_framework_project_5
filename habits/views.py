from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitListPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsHabitOwner


class HabitCreateAPIView(generics.CreateAPIView):
    """Класс generics модели Habit для создания привычки."""

    serializer_class = HabitSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        """Метод добавляет в поле owner пользователя, который создает урок."""

        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitListAPIView(generics.ListAPIView):
    """Класс generics модели Habit для вывода списка привычек."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitListPaginator


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Класс generics модели Habit для вывода информации о привычке."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsHabitOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Класс generics модели Habit для обновления информации о привычке."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsHabitOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Класс generics модели Habit для удаления привычки."""

    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsHabitOwner]
