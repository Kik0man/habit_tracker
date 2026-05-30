from django.test import TestCase
from unittest.mock import patch, MagicMock
from habits.tasks import send_habit_reminders
from habits.models import Habit
from django.contrib.auth import get_user_model

User = get_user_model()

class TasksTest(TestCase):
    @patch('habits.tasks.send_telegram_message')
    def test_send_habit_reminders_no_crash(self, mock_send):
        user = User.objects.create_user(username='tester', password='pass')
        # Добавьте поле telegram_chat_id, если есть, иначе просто проверяем выполнение
        habit = Habit.objects.create(
            user=user,
            place='home',
            time='12:00:00',
            action='meditate',
            duration=10,
            periodicity=1
        )
        # Задача не должна упасть
        send_habit_reminders()
        self.assertTrue(True)