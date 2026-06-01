from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from habits.models import Habit

User = get_user_model()

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.pleasant = Habit.objects.create(
            user=self.user, place='home', time='12:00', action='relax',
            is_pleasant=True, duration=30, periodicity=1
        )

    def test_duration_cannot_exceed_120(self):
        habit = Habit(
            user=self.user, place='home', time='12:00', action='run',
            duration=130, periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_cannot_have_both_reward_and_related(self):
        habit = Habit(
            user=self.user, place='home', time='12:00', action='run',
            duration=60, reward='candy', related_habit=self.pleasant, periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_related_habit_must_be_pleasant(self):
        not_pleasant = Habit.objects.create(
            user=self.user, place='office', time='09:00', action='work',
            is_pleasant=False, duration=60, periodicity=1
        )
        habit = Habit(
            user=self.user, place='home', time='18:00', action='meditate',
            duration=60, related_habit=not_pleasant, periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_cannot_have_reward(self):
        habit = Habit(
            user=self.user, place='home', time='12:00', action='nap',
            is_pleasant=True, reward='chocolate', duration=30, periodicity=1
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_periodicity_between_1_and_7(self):
        habit = Habit(
            user=self.user, place='home', time='12:00', action='read',
            duration=60, periodicity=8
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()


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


    def test_serializer_validates_reward_and_related(self):
        data = {
            'place': 'gym', 'time': '08:00', 'action': 'workout',
            'duration': 60, 'reward': 'smoothie', 'related_habit': self.pleasant.id,
            'periodicity': 1, 'user': self.user.id
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())