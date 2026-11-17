from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, EmailVerification

# Create your tests here.
class AccountsTestCase(TestCase):

    # def setup 
    def setUp(self):
        self.client = APIClient()
    
    self.account = {
        "username" : "deeja",
        "first_name" : "khadija",
        "last_name" : "ismail",
        "email" : "sadiqismail@gmail.com",
        "password" : "StrongPassword123",
        "confirm_password" : "StrongPassword123"
    }

    self.user = User.objects.create(username="sadiq", first_name="bashir", last_name="musa", email="bashirmusa@gmail.com", is_verified=False)
    self.user.set_password("Strong454")
    self.user.save()
    self.verification = EmailVerification.objects.create(user=self.user, otp="234567")
    self.verification1 = EmailVerification.objects.create(user=self.user, otp='345678')

    reset_password = {
        "email" : "bashirmusa@gmail.com",
        "otp" : '345678',
        "password" : "StrongPassword123"
    }
    # test account creation
    def test_create_account(self):
        response = self.client.post(reverse("register_view"), data=self.account, format='json')
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='sadiqismail@gmail.com')
        self.assertTrue(user.check_password("StrongPassword123"))
        self.assertTrue(EmailVerification.objects.filter(user=user).exists)

    # test duplicate account creation
    def test_bad_account(self):
        response = self.client.post(reverse("register_view"), data=self.account, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test user verification
    def test_otp_verification(self):
        response = self.client.post(reverse("verify_otp"), data={"email" : self.user.email, "otp" : "234567"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data= response.json()
        self.assertEqual(data['message'], "User verification is successful")
        self.assertTrue(self.user.is_verified)

    # test user login 
    def test_login(self):
        response = self.client.post(reverse("login_view"), data={"email" : "bashirmusa@gmail.com", "password" : "Strong454"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['message'], "Login Successful")

    def  test_forget_reset_password(self):
        response = self.client.post(reverse("forget_password"), data={"email" : self.user.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['message'], "Email Sent successfully")
        self.assertTrue(EmailVerification.objects.get(user=user))

        response = self.client.post(reverse("reset_password"), data=reset_password, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password("StrongPassword123"))
