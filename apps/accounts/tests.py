from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import User


class AccountsAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.dashboard_url = reverse('accounts:dashboard')
        self.user_password = 'TestPassword123!'
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@orient.com.bd',
            password=self.user_password,
            first_name='Existing',
            last_name='User',
            phone='+8801700000000',
            role='customer'
        )

    def test_successful_registration(self):
        """Test creating a new customer account successfully."""
        data = {
            'username': 'newcustomer',
            'first_name': 'New',
            'last_name': 'Customer',
            'email': 'newcustomer@orient.com.bd',
            'phone': '+8801711111111',
            'password1': 'StrongPass123!#',
            'password2': 'StrongPass123!#',
        }
        response = self.client.post(self.register_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.dashboard_url)
        
        # Verify user was created in DB
        user = User.objects.filter(username='newcustomer').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newcustomer@orient.com.bd')
        self.assertEqual(user.role, 'customer')

        # Verify success message
        messages = list(response.context['messages'])
        self.assertTrue(any('Welcome to Orient Computers' in str(m) for m in messages))

    def test_registration_duplicate_email(self):
        """Test registration fails with clear error when email already exists."""
        data = {
            'username': 'uniqueuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'existing@orient.com.bd',  # Duplicate email
            'phone': '+8801722222222',
            'password1': 'StrongPass123!#',
            'password2': 'StrongPass123!#',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='uniqueuser').exists())
        self.assertContains(response, 'An account with this email address already exists.')

    def test_registration_password_mismatch(self):
        """Test registration fails with clear error when passwords don't match."""
        data = {
            'username': 'mismatchuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'mismatch@orient.com.bd',
            'phone': '+8801722222222',
            'password1': 'StrongPass123!#',
            'password2': 'DifferentPass123!#',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())
        self.assertTrue('password2' in response.context['form'].errors)

    def test_login_with_username(self):
        """Test logging in using username."""
        data = {
            'username': 'existinguser',
            'password': self.user_password,
        }
        response = self.client.post(self.login_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, 'existinguser')

    def test_login_with_email(self):
        """Test logging in using email address (case-insensitive)."""
        data = {
            'username': 'EXISTING@orient.com.bd',
            'password': self.user_password,
        }
        response = self.client.post(self.login_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, 'existinguser')

    def test_login_with_invalid_credentials(self):
        """Test login with incorrect password shows invalid credentials error."""
        data = {
            'username': 'existinguser',
            'password': 'WrongPassword123',
        }
        response = self.client.post(self.login_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
        messages = list(response.context['messages'])
        self.assertTrue(any('Invalid username/email or password' in str(m) for m in messages))
