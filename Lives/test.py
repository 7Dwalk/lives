from django.test import TestCase, Client
from django.contrib.auth.models import User


class RegistrationTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.url = '/signup/'
        cls.valid_data = {'username': 'testuser',
                          'email':    'test@example.com',
                          'password': 'testpassword'}
        cls.existing_username_data = {'username': 'existinguser',
                                      'email':    'test@example.com',
                                      'password': 'testpassword'}
        cls.existing_email_data = {'username': 'testuser',
                                   'email':    'existing@example.com',
                                   'password': 'testpassword'}

    def test_registration_success(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'success': True, 'message': 'Registration successful'})
        self.assertTrue(User.objects.filter(
            username=self.valid_data['username']).exists())

    def test_registration_duplicate_username(self):
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword')

        response = self.client.post(self.url, self.existing_username_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'success': False, 'message': 'Username already exists'})
        self.assertFalse(User.objects.filter(
            email=self.existing_username_data['email']).exists())

    def test_registration_duplicate_email(self):
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword')

        response = self.client.post(self.url, self.existing_email_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'success': False, 'message': 'Email already exists'})
        self.assertFalse(User.objects.filter(
            username=self.existing_email_data['username']).exists())


class LoginTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.url = '/login/'
        cls.valid_data = {'username': 'testuser',
                          'password': 'testpassword'}
        cls.invalid_username_data = {'username': 'nonexistentuser',
                                     'password': 'testpassword'}
        cls.invalid_password_data = {'username': 'testuser',
                                     'password': 'wrongpassword'}

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username=self.valid_data['username'],
            email='test@example.com',
            password=self.valid_data['password'])
        self.client.login(username=self.user.username,
                          password=self.user.password)

    def test_login_success(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'success': True, 'message': 'Login successful'})

    def test_login_invalid_username(self):
        response = self.client.post(self.url, self.invalid_username_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'success': False, 'message': 'Invalid username'})

    def test_login_invalid_password(self):
        response = self.client.post(self.url, self.invalid_password_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'success': False, 'message': 'Invalid password'})

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        self.user.refresh_from_db()
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
                             'success': False, 'message': 'Unable to login'})
