
from django.test import TestCase
from django.core import mail
from .models import User
from .views import send_verification_email  # Assuming the email sending function is in views.py
import asyncio

class SendVerificationEmailTest(TestCase):

    def setUp(self):
        # Setup user for testing
        self.user = User.objects.create(username='testuser', name='Test User', email='testuser@example.com', password='testpassword')

    def test_send_verification_email(self):
        # Call the asynchronous send email function
        asyncio.run(self.user.send_verification_email(self.user.email))  # Assuming the function is asynchronous

        # Check if the email was sent
        self.assertEqual(len(mail.outbox), 1)  # Only 1 email should be sent
        email = mail.outbox[0]

        # Check email subject and body
        self.assertEqual(email.subject, 'Email Verification')
        self.assertIn('Please click the link to verify your email.', email.body)

        # Check if the email was sent to the correct recipient
        self.assertEqual(email.to, [self.user.email])

