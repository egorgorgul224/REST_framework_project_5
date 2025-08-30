from rest_framework import serializers

from habits.models import Habit
from habits.validators import IsNiceRelatedHabitValidator, NiceHabitValidator, RelatedHabitOrRewardValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализация модели Habit. Предоставлен доступ ко всем полям, кроме owner."""

    validators = [
        NiceHabitValidator(is_nice_habit="is_nice_habit", related_habit="related_habit", reward="reward"),
        RelatedHabitOrRewardValidator(related_habit="related_habit", reward="reward"),
        IsNiceRelatedHabitValidator(related_habit="related_habit"),
    ]

    class Meta:
        model = Habit
        exclude = ["owner"]


class HabitInfoSerializer(serializers.ModelSerializer):
    """Сериализация модели Habit. Предоставлен доступ к полям place, time, action, periodicity, reward, execute_time.
    Используется в контроллере для отображения привычек в общем доступе."""

    validators = [
        NiceHabitValidator(is_nice_habit="is_nice_habit", related_habit="related_habit", reward="reward"),
        RelatedHabitOrRewardValidator(related_habit="related_habit", reward="reward"),
        IsNiceRelatedHabitValidator(related_habit="related_habit"),
    ]

    class Meta:
        model = Habit
        fields = ["place", "time", "action", "periodicity", "reward", "execute_time"]
