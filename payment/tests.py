from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Transfer
from django.contrib.auth.models import User
from account.models import Account


class TransferTestsAdmin(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('superuser', 'superuser@test.com', 'test')
        self.client.login(username='superuser', password='test')
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TransferTestsUser(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@gmail.com', password="pass")
        self.client.login(username='user', password='pass')
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
