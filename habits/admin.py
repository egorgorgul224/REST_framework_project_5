from django.contrib import admin

from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Админ панель по привычкам. Поля для отображения: action, place, time, owner. Поле для фильтра: place, time.
    Поле для поиска: action, place."""

    list_display = ("action", "place", "time", "owner")
    list_filter = ("place", "time")
    search_fields = ("action", "place")
