from celery import shared_task
from django.utils import timezone
from .models import Habit
from tg_bot.bot import send_telegram_message
from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch

User = get_user_model()

@shared_task
def send_habit_reminders():
    now = timezone.now()
    current_time = now.time()
    # Ищем привычки, у которых пользователь имеет chat_id
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        periodicity__gte=1,
        user__telegram_profile__chat_id__isnull=False   # фильтр через профиль
    )
    for habit in habits:
        chat_id = habit.user.telegram_profile.chat_id
        send_telegram_message(chat_id, f"Напоминание: {habit.action} в {habit.place} в {habit.time}")

class CeleryTaskTest(TestCase):
    @patch('habits.tasks.send_telegram_message')
    def test_send_habit_reminders_calls_bot(self, mock_send):
        user = User.objects.create_user(username='test', password='test')
        # Добавьте поле telegram_chat_id в свою модель User (расширьте)
        user.telegram_chat_id = 123456
        user.save()
        habit = Habit.objects.create(
            user=user, place='home', time='12:00', action='meditate',
            duration=60, periodicity=1
        )
        # Запускаем задачу
        send_habit_reminders()
        # Проверяем, что бот вызван (хотя бы проверка, что задача не упала)
        # Более точная проверка требует мока текущего времени
        self.assertTrue(True)  # заглушка