from rest_framework.pagination import PageNumberPagination


class HabitListPaginator(PageNumberPagination):
    """Пагинатор для вывода списка привычек. Выводит 5 элементов на страницу."""

    page_size = 5
    page_size_query_param = "page_size"
