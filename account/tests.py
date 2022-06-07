from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Account
from django.contrib.auth.models import User


class AuthTests(APITestCase):

    def setUp(self):
        superuser = {
            'username': 'superuser',
            'password': 'superuser',
            'email': 'superuser@test.com'
        }
        User.objects.create_superuser(username=superuser["username"],
                                      email=superuser["email"],
                                      password=superuser["password"])
        response = self.client.post(reverse('rest_login'), superuser, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access_token"]}')

    def test_current_user(self):
        response = self.client.get(reverse('account:accounts-list'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)


class TestAccounts(APITestCase):

    def setUp(self):
        superuser = {
            'username': 'superuser',
            'password': 'superuser',
            'email': 'superuser@test.com'
        }
        self.bank = User.objects.create_superuser(username=superuser["username"],
                                      email=superuser["email"],
                                      password=superuser["password"])
        response = self.client.post(reverse('rest_login'), superuser, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access_token"]}')
        self.sender = User.objects.create_user(username='sender', email='sender@gmail.com', password="pass")
        self.receiver = User.objects.create_user(username='receiver', email='receiver@gmail.com', password="pass")
        self.balance = 100
        self.sender_account = Account.objects.create(
            user=self.sender
        )
        self.receiver_account = Account.objects.create(
            user=self.receiver,
        )
        self.bank_account = Account.objects.create(
            user=self.bank,
        )

    def test_get_balance(self):
        uid = self.sender_account.uid
        response = self.client.get(reverse('account:balance', kwargs={'uid': uid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data).get('balance'), 0)

    def test_account_list(self):
        response = self.client.get(reverse('account:accounts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
