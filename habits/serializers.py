from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализация модели Habit. Предоставлен доступ ко всем полям, кроме owner."""

    class Meta:
        model = Habit
        exclude = ["owner"]
