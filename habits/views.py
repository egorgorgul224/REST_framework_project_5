from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitListPaginator
from habits.serializers import HabitInfoSerializer, HabitSerializer
from users.permissions import IsHabitOwner


class HabitCreateAPIView(generics.CreateAPIView):
    """Класс generics модели Habit для создания привычки."""

    serializer_class = HabitSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        """Метод добавляет в поле owner пользователя, который создает привычку. В поле day_counter передается значение
        поля периодичности."""

        habit = serializer.save()
        habit.owner = self.request.user
        habit.day_counter = habit.periodicity
        habit.save()


class HabitListAPIView(generics.ListAPIView):
    """Класс generics модели Habit для вывода списка привычек."""

    serializer_class = HabitInfoSerializer
    pagination_class = HabitListPaginator

    def get_queryset(self):
        """Функция для получения списка привычек. Если админ - то все привычки, пользователь - только свои."""

        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(owner=self.request.user.id)


class HabitPublishedListAPIView(generics.ListAPIView):
    """Класс generics модели Habit для вывода списка привычек, опубликованных в общий доступ."""

    serializer_class = HabitInfoSerializer
    pagination_class = HabitListPaginator

    def get_queryset(self):
        """Функция для получения списка привычек. Если админ - то все привычки, пользователь - только опубликованные в
        общий доступ."""

        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(is_published=True)


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

    def perform_update(self, serializer):
        """Метод обновляет поле day_counter значение поля периодичности."""

        habit = serializer.save()
        habit.day_counter = habit.periodicity
        habit.save()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Класс generics модели Habit для удаления привычки."""

    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsHabitOwner]
