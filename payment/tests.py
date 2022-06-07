from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Transfer
from django.contrib.auth.models import User
from account.models import Account


class TransferTestsAdmin(APITestCase):

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
        self.sender = User.objects.create_user(username='sender', email='sender@gmail.com', password="pass")
        self.receiver = User.objects.create_user(username='receiver', email='receiver@gmail.com', password="pass")
        self.balance = 100
        self.sender_account = Account.objects.create(
            user=self.sender,
            balance=self.balance,
        )
        self.receiver_account = Account.objects.create(
            user=self.receiver,
            balance=self.balance,
        )
        self.url = reverse('payment:transfer')

    def test_get_all_transfers(self):
        """
        Super user : show all transfers
        :return:
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_sender_receiver(self):
        accounts = Account.objects.count()
        self.assertEqual(accounts, 2)

    def test_transfer_normal(self):
        """
        Super user : transfer normal
        """
        data = {
            "uid_sender": self.sender_account.uid,
            "uid_receiver": self.receiver_account.uid,
            "amount": 10.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        sender = self.client.get(reverse('account:balance', kwargs={'uid': self.sender_account.uid}))
        receiver = self.client.get(reverse('account:balance', kwargs={'uid': self.receiver_account.uid}))
        self.assertEqual(float(sender.data['balance']), 90.0)
        self.assertEqual(float(receiver.data['balance']), 110.0)

    def test_transfer_more_then_balance_sender(self):
        """
        Super user : transfer > balance sender
        """
        data = {
            "uid_sender": self.sender_account.uid,
            "uid_receiver": self.receiver_account.uid,
            "amount": 1000.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_transfer_null_value(self):
        """
        Super user  : null value
        """
        data = {
            "uid_sender": self.sender_account.uid,
            "uid_receiver": self.receiver_account.uid,
            "amount": 0.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer_missing_key(self):
        """
        Super user : missing key
        """
        data = {
            "uid_sender": self.sender_account.uid,
            "amount": 0.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TransferTestsAnonymous(APITestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username='sender', email='sender@gmail.com', password="pass")
        self.receiver = User.objects.create_user(username='receiver', email='receiver@gmail.com', password="pass")
        self.balance = 100
        self.sender_account = Account.objects.create(
            user=self.sender,
            balance=self.balance,
        )
        self.receiver_account = Account.objects.create(
            user=self.receiver,
            balance=self.balance,
        )
        self.url = reverse('payment:transfer')

    def test_get_all_transfers(self):
        """
        Anonymous : show all transfers
        :return:
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_transfer_normal(self):
        """
        Anonymous : transfer normal
        """
        data = {
            "uid_sender": self.sender_account.uid,
            "uid_receiver": self.receiver_account.uid,
            "amount": 10.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TransferTestsUser(APITestCase):

    def setUp(self):
        user = {
            'username': 'user',
            'password': 'user',
            'email': 'user@test.com'
        }
        User.objects.create_user(username=user["username"],
                                      email=user["email"],
                                      password=user["password"])
        response = self.client.post(reverse('rest_login'), user, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access_token"]}')
        self.sender = User.objects.create_user(username='sender', email='sender@gmail.com', password="pass")
        self.receiver = User.objects.create_user(username='receiver', email='receiver@gmail.com', password="pass")
        self.balance = 100
        self.sender_account = Account.objects.create(
            user=self.sender,
            balance=self.balance,
        )
        self.receiver_account = Account.objects.create(
            user=self.receiver,
            balance=self.balance,
        )
        self.url = reverse('payment:transfer')

    def test_get_all_transfers(self):
        """
        User : show all transfers
        :return:
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_transfer_normal(self):
        """
        User : transfer normal
        """
        data = {
            "uid_sender": self.sender_account.uid,
            "uid_receiver": self.receiver_account.uid,
            "amount": 10.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
