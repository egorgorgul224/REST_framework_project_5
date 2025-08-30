from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (HabitCreateAPIView, HabitDestroyAPIView, HabitListAPIView, HabitPublishedListAPIView,
                          HabitRetrieveAPIView, HabitUpdateAPIView)

app_name = HabitsConfig.name

urlpatterns = [
    # ссылки для модели Habit
    path("habit/create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path("habits/", HabitListAPIView.as_view(), name="habit_list"),
    path("published/habits/", HabitPublishedListAPIView.as_view(), name="habit_published_list"),
    path("habit/<int:pk>/detail/", HabitRetrieveAPIView.as_view(), name="habit_detail"),
    path("habit/<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("habit/<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habit_delete"),
]
