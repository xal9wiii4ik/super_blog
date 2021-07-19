import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.user_profile.serializers import AccountModelSerializer


class AccountApiTestCase(APITestCase):
    """
    Api test for account
    """

    def setUp(self) -> None:
        password = make_password('password')
        url = reverse('token')

        self.user = get_user_model().objects.create(username='first user',
                                                    password=password,
                                                    gender='male',
                                                    phone='12312321',
                                                    email='check@yandex.ru',
                                                    is_active=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = f"Token " \
                     f"{self.client.post(path=url, data=json_data, content_type='application/json').data['access']}"

        self.user_1 = get_user_model().objects.create(username='second user',
                                                      password=password,
                                                      gender='female',
                                                      phone='87878127',
                                                      is_active=True)
        data_1 = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = f"Token " \
                       f"{self.client.post(path=url, data=json_data_1, content_type='application/json').data['access']}"

    def test_get(self) -> None:
        """
        get list of accounts
        """

        url = reverse('user_profile:account-list')
        accounts = get_user_model().objects.all()
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(AccountModelSerializer(accounts, many=True).data,
                         response.data)

    def test_get_retrieve(self) -> None:
        """
        Get one account
        """

        url = reverse('user_profile:account-detail', args=(self.user.pk,))
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.assertEqual(AccountModelSerializer(self.user).data,
                         response.data)

    def test_create(self) -> None:
        """
        Create new account
        """

        self.assertEqual(first=2, second=get_user_model().objects.all().count())
        url = reverse('user_profile:account-list')
        data = {
            'username': 'third_user',
            'password': 'third_password123123',
            'repeat_password': 'third_password123123',
            'gender': 'male',
            'phone': '90909090901',
            'email': 'new_email@yandex.ru'
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.assertEqual(first=3, second=get_user_model().objects.all().count())

    def test_create_bad_email(self) -> None:
        """
        Create new account with bad email
        """

        self.assertEqual(first=2, second=get_user_model().objects.all().count())
        url = reverse('user_profile:account-list')
        data = {
            'username': 'third_user',
            'password': 'third_password123123',
            'gender': 'male',
            'phone': '90909090901',
            'email': 'check@yandex.ru'
        }
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(first=status.HTTP_400_BAD_REQUEST, second=response.status_code)
        self.assertEqual(first=2, second=get_user_model().objects.all().count())

    def test_update(self) -> None:
        """
        Update account
        """

        self.assertEqual(first='first user', second=self.user.username)
        url = reverse('user_profile:account-detail', args=(self.user.pk,))
        data = {
            'username': 'new_username',
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(path=url, data=data, format='multipart')
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.user.refresh_from_db()
        self.assertEqual(first='new_username', second=self.user.username)

    def test_update_bad_not_owner(self) -> None:
        """
        Update account with bad credentials (403)
        """

        url = reverse('user_profile:account-detail', args=(self.user.pk,))
        data = {
            'username': 'new_username',
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.patch(path=url, data=data, format='multipart')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_delete(self) -> None:
        """
        Delete account
        """

        self.assertEqual(first=2, second=get_user_model().objects.all().count())
        url = reverse('user_profile:account-detail', args=(self.user.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=1, second=get_user_model().objects.all().count())

    def test_delete_now_owner(self) -> None:
        """
        Delete account with bad credentials (401)
        """

        url = reverse('user_profile:account-detail', args=(self.user.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
