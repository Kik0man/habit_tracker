from unittest import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

User = get_user_model()

class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', password='secret')
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place='gym',
            time='08:00:00',
            action='workout',
            duration=60,
            periodicity=1,
            is_public=False
        )

    def test_list_habits(self):
        """Пользователь видит только свои привычки (пагинация по 5)"""
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_habit_valid(self):
        data = {
            'place': 'home',
            'time': '21:00:00',
            'action': 'read book',
            'duration': 30,
            'periodicity': 1
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_create_habit_invalid_duration(self):
        data = {
            'place': 'home', 'time': '21:00:00', 'action': 'read',
            'duration': 130, 'periodicity': 1
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('120', str(response.data['non_field_errors']))

    def test_retrieve_own_habit(self):
        response = self.client.get(f'/api/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'workout')

    def test_update_own_habit(self):
        data = {
            'place': 'park',
            'time': '07:00:00',
            'action': 'jogging',
            'duration': 45,
            'periodicity': 1
        }
        response = self.client.put(f'/api/habits/{self.habit.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'jogging')

    def test_delete_own_habit(self):
        response = self.client.delete(f'/api/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_cannot_access_another_users_habit(self):
        other_user = User.objects.create_user(username='jane', password='pass')
        other_habit = Habit.objects.create(
            user=other_user,
            place='office',
            time='09:00:00',
            action='code',
            duration=120,
            periodicity=1
        )
        response = self.client.get(f'/api/habits/{other_habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habits_list(self):
        public_habit = Habit.objects.create(
            user=self.user,
            place='square',
            time='10:00:00',
            action='yoga',
            duration=60,
            periodicity=1,
            is_public=True
        )
        # Другой пользователь
        stranger = User.objects.create_user(username='stranger', password='x')
        self.client.force_authenticate(user=stranger)
        response = self.client.get('/api/habits/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], 'yoga')



class PermissionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='perm_owner', password='pass')
        self.other = User.objects.create_user(username='perm_other', password='pass')
        self.habit = Habit.objects.create(
            user=self.user,
            place='home',
            time='12:00:00',
            action='sleep',
            duration=30,
            periodicity=1
        )
        self.permission = IsOwnerOrReadOnly()
        self.factory = APIRequestFactory()

    def test_owner_can_edit(self):
        request = self.factory.put('/')
        request.user = self.user
        has_perm = self.permission.has_object_permission(request, APIView(), self.habit)
        self.assertTrue(has_perm)
