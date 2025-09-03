from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from config import settings


# Create your models here.
class Habit(models.Model):
    """Модель привычка. Содержит поля place, time, action, is_nice_habit(по умолчанию false), related_habit,
    periodicity, reward, execute_time, is_published(по умолчанию false), owner, day_counter."""

    place = models.CharField(
        max_length=50,
        verbose_name="Место, где выполняется привычка",
        help_text="Введите место, где выполняется привычка",
    )
    time = models.TimeField(verbose_name="Время выполнения привычки", help_text="Укажите время выполнения привычки")
    action = models.TextField(verbose_name="Действие, которое необходимо сделать", help_text="Введите действие")
    is_nice_habit = models.BooleanField(default=False, verbose_name="Выбрать, если привычка приятная")
    related_habit = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="habits", null=True, blank=True)
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность выполнения",
        help_text="Укажите периодичность выполнения привычки(дни)",
        validators=[MaxValueValidator(7), MinValueValidator(1)],
    )
    reward = models.TextField(
        null=True,
        blank=True,
        verbose_name="Награда после выполнения привычки",
        help_text="Укажите награду после выполнения привычки",
    )
    execute_time = models.PositiveIntegerField(
        default=120,
        verbose_name="Время выполнения(секунды)",
        help_text="Укажите время выполнения привычки(секунды)",
        validators=[MaxValueValidator(120), MinValueValidator(1)],
    )
    is_published = models.BooleanField(default=False, verbose_name="Выбрать для публикации в общий доступ")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="habits", blank=True, null=True
    )
    day_counter = models.PositiveIntegerField(default=1, verbose_name="Счетчик периодичности")

    def __str__(self):
        return f"Привычка: действие - {self.action}, время - {self.time}, место - {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["time"]
