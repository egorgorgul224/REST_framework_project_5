from rest_framework.serializers import ValidationError


class NiceHabitValidator:
    """Класс-валидатор для определения, что привычка является приятной. У такой привычки не может быть указана
    связанная привычка и/или вознаграждение."""

    def __init__(self, is_nice_habit, related_habit, reward):
        self.is_nice_habit = is_nice_habit
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, value):
        is_nice_habit = value.get(self.is_nice_habit)
        related_habit = value.get(self.related_habit)
        reward = value.get(self.reward)
        if is_nice_habit:
            if related_habit or reward:
                raise ValidationError("Для приятной привычки нельзя указать вознаграждение и связанную привычку.")


class RelatedHabitOrRewardValidator:
    """Класс-валидатор для определения, что для полезной привычки можно указать связанную приятную привычку или
    вознаграждение."""

    def __init__(self, related_habit, reward):
        self.related_habit = related_habit
        self.reward = reward

    def __call__(self, value):
        related_habit = value.get(self.related_habit)
        reward = value.get(self.reward)
        if related_habit:
            if reward:
                raise ValidationError(
                    "Для полезной привычки можно указать только связанную привычку или вознаграждение."
                )


class IsNiceRelatedHabitValidator:
    """Класс-валидатор для определения, что связанная привычка является приятной. Запрещено для полезной привычки
    выбирать полезную привычку."""

    def __init__(self, related_habit):
        self.related_habit = related_habit

    def __call__(self, value):
        related_habit = value.get(self.related_habit)
        if related_habit:
            if not related_habit.is_nice_habit:
                raise ValidationError("Для полезной привычки можно выбрать только приятную привычку.")
