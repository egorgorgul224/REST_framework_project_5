from django.contrib import admin

from users.models import User


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    """Админ панель с пользователями. Поля для отображения: id, email. Поля для поиска: email, tg_chat_id."""

    list_display = ("id", "email")
    search_fields = ("email", "tg_chat_id")
