from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from habits.models import Habit
from habits.serializers import HabitSerializer

User = get_user_model()

class HabitSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.pleasant = Habit.objects.create(
            user=self.user, place='home', time='12:00', action='sleep',
            is_pleasant=True, duration=30, periodicity=1
        )

    def test_serializer_validates_duration(self):
        data = {
            'place': 'gym', 'time': '08:00', 'action': 'workout',
            'duration': 150, 'periodicity': 1, 'user': self.user.id
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertIn('120', str(serializer.errors))

    def test_serializer_validates_reward_and_related(self):
        data = {
            'place': 'gym', 'time': '08:00', 'action': 'workout',
            'duration': 60, 'reward': 'smoothie', 'related_habit': self.pleasant.id,
            'periodicity': 1, 'user': self.user.id
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_create_with_related_habit(self):
        data = {
            'place': 'pool',
            'time': '18:00:00',
            'action': 'swim',
            'duration': 45,
            'periodicity': 1,
            'related_habit': self.pleasant.id,
            'reward': None
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # должно быть валидно