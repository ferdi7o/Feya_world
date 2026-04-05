from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@test.com')

    def test_user_creation(self):
        """1. Проверка дали потребителят е създаден успешно."""
        self.assertEqual(self.user.username, 'testuser')

    def test_profile_auto_creation(self):
        """2. Проверка дали профилът се създава автоматично при регистрация."""
        self.assertTrue(hasattr(self.user, 'profile'))

    def test_login_view(self):
        """3. Проверка дали страницата за вход е достъпна."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        """4. Проверка дали потребителят може да влезе с правилни данни."""
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)

    def test_profile_view_requires_login(self):
        """5. Проверка дали страницата на профила изисква вход i vhod za nacalna stranitsa."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    # + 10 tests on the products/tests.py