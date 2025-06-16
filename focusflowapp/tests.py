from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Habit, HabitEntry
import datetime

class AuthTests(APITestCase):
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_fails(self):
        response = self.client.post(reverse('register'), {
            'username': 'test',
            'email': 'test@example.com',
            'password': ''
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_login_returns_token(self):
        user = User.objects.create_user(username='tester', password='1234')
        response = self.client.post(reverse('login'), {
            'username': 'tester',
            'password': '1234'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class HabitTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='sedii', password='1234')
        response = self.client.post(reverse('login'), {
            'username': 'sedii',
            'password': '1234'
        })
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

     # --- CREATE (POST) ---
    def test_create_habit_success(self):
        url = reverse('habit-list')
        data = {'name': 'Read', 'goal_per_day': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)

    def test_create_habit_invalid_data(self):
        url = reverse('habit-list')
        data = {'name': '', 'goal_per_day': -1}  # Невалидни данни
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- READ (GET) ---
    def test_get_habit_list(self):
        Habit.objects.create(name='Run', goal_per_day=1, user=self.user)
        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_nonexistent_habit(self):
        url = reverse('habit-detail', kwargs={'pk': 999})  # Несъществуващ ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- UPDATE (PUT/PATCH) ---
    def test_update_habit_success(self):
        habit = Habit.objects.create(name='Meditate', goal_per_day=1, user=self.user)
        url = reverse('habit-detail', kwargs={'pk': habit.id})
        data = {'name': 'Meditate Daily', 'goal_per_day': 2}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.name, 'Meditate Daily')

    def test_update_other_users_habit_fails(self):
        other_user = User.objects.create_user(username='other', password='12345')
        habit = Habit.objects.create(name='Swim', goal_per_day=1, user=other_user)
        url = reverse('habit-detail', kwargs={'pk': habit.id})
        data = {'name': 'Hacked', 'goal_per_day': 99}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # или 404

    # --- DELETE (DELETE) ---
    def test_delete_habit_success(self):
        habit = Habit.objects.create(name='Sleep', goal_per_day=1, user=self.user)
        url = reverse('habit-detail', kwargs={'pk': habit.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_delete_other_users_habit_fails(self):
        other_user = User.objects.create_user(username='other', password='12345')
        habit = Habit.objects.create(name='Yoga', goal_per_day=1, user=other_user)
        url = reverse('habit-detail', kwargs={'pk': habit.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HabitEntryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='sedii', password='1234')
        response = self.client.post(reverse('login'), {
            'username': 'sedii',
            'password': '1234'
        })
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        self.habit = Habit.objects.create(
                name='Drink Water',
                goal_per_day=8,
                user=self.user
            )
        self.today = datetime.date.today()
        

    def test_create_habit_entry_success(self):
        url = reverse('habit-entry-list')
        data = {
            'habit': self.habit.name, 
            'date': self.today,
            'completed_count': 5
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HabitEntry.objects.count(), 1)
        entry = HabitEntry.objects.first()
        self.assertEqual(entry.habit, self.habit)
        self.assertEqual(entry.date, self.today)
        self.assertEqual(entry.completed_count, 5)

    def test_create_habit_entry_invalid_data(self):
        url = reverse('habit-entry-list')
        data = {
            'habit': 5, 
            'date': 3,
            'completed_count': "test"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(HabitEntry.objects.count(), 0)

    def test_create_habit_entry_no_token(self):
        url = reverse('habit-entry-list')
        data = {
            'habit': self.habit.name, 
            'date': self.today,
            'completed_count': 5
        }

        self.client.credentials()

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(HabitEntry.objects.count(), 0)

    def test_get_habit_entry_list(self):
        url = reverse('habit-entry-list')
        HabitEntry.objects.create(
            habit=self.habit, 
            date=self.today,
            completed_count=5)
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


# More to come