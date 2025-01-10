"""Tests for User Profile Model"""


from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    """Test Models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user using email id is successful."""
        email = "test@example.com"
        first_name = "Test"
        last_name = "User"
        password = "something"
        user = get_user_model().objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.get_full_name(), first_name + " " + last_name)
        self.assertEqual(user.get_short_name(), first_name)
        self.assertTrue(user.check_password(password))

    def test_email_normalisation(self):
        """Test that new email ids are getting normalized."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                first_name='Test',
                password='default123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that email address is a required field"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                first_name='Test',
                password='test123'
            )

    def test_new_user_without_firstname_raises_error(self):
        """Test that first name is a required field"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='test@example.com',
                first_name='',
                password='test123',
            )

    def test_create_superuser(self):
        """Test creating a Super User."""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            first_name='Admin',
            password='test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
