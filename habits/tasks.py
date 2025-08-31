import datetime

from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_message_to_telegram():
    """Функция для получения привычек по времени и отправки оповещений по привычкам в телеграм. Задача вызывается
    каждый час и оправляет привычки в период этого часа(например задача запускается в 11:00, привычки от 11:00 до
    11:59)."""

    current_time = datetime.datetime.now().time().hour
    start = f"{current_time}:00"
    finish = f"{current_time}:59"
    habits = Habit.objects.filter(is_nice_habit=False, time__range=(start, finish))
    for habit in habits:
        habit.day_counter -= 1
        if not habit.day_counter:
            if habit.owner.tg_chat_id:
                message = f"Необходимо выполнить привычку: {habit.action}, время: {habit.time}, место: {habit.place}. Время на выполнение привычки: {habit.execute_time} сек."
                send_telegram_message(message=message, chat_id=habit.owner.tg_chat_id)
                habit.day_counter = habit.periodicity
                habit.save(update_fields=["day_counter"])
        habit.save(update_fields=["day_counter"])
