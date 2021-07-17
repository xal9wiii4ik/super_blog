import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from apps.user_profile.services_views import _create_unique_uid, _current_ip_port, updating_account
from apps.user_profile.models import Uid


def get_request():
    url = reverse('token')
    factory = APIRequestFactory()
    return factory.get(url)


class ServicesViewsTestCase(APITestCase):
    """
    Test Case for services
    """

    def setUp(self) -> None:
        password = make_password('password')
        new_password = make_password('new_password')

        self.uid_1 = Uid.objects.create(uid=uuid.uuid1(), user_id=1, updated_data='xal9wa@gmail.com')
        self.uid_2 = Uid.objects.create(uid=uuid.uuid1(), user_id=1, updated_data=new_password)
        self.user = get_user_model().objects.create(username='first user_s',
                                                    password=password,
                                                    gender='male',
                                                    phone='12312321',
                                                    email='check@yandex.ru',
                                                    is_active=False)

    def test_create_unique_uid(self) -> None:
        """
        Test for creating unique uid object
        """

        self.assertEqual(first=Uid.objects.all().count(), second=2)
        _create_unique_uid(user_id=1)
        self.assertEqual(first=Uid.objects.all().count(), second=3)

    def test_current_ip_port(self) -> None:
        """
        Test fir getting current url
        """

        request = get_request()
        url = _current_ip_port(is_secure=request.is_secure(), host=request.get_host(), url='/check/')
        self.assertEqual(first='http://testserver/check/', second=url)

    def test_updating_account_activate(self) -> None:
        """
        Test for updating account; ACTION=activate
        """

        self.assertFalse(self.user.is_active)
        updating_account(uid=self.uid_1.uid.hex, user_id=1, action='activate')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_updating_account_bad(self) -> None:
        """
        Test for updating account; ACTION=activate; BAD UID
        """

        self.assertFalse(self.user.is_active)
        updating_account(uid='sefbnsefnlwefnlkewfjnlkewjfelwi', user_id=1, action='activate')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_updating_account_update_account(self) -> None:
        """
        Test for updating account; ACTION=update_account
        """

        self.assertEqual(first='check@yandex.ru', second=self.user.email)
        updating_account(uid=self.uid_1.uid.hex, user_id=1, action='update_account')
        self.user.refresh_from_db()
        self.assertEqual(first='xal9wa@gmail.com', second=self.user.email)

    def test_updating_account_reset_password(self) -> None:
        """
        Test for updating account; ACTION=reset_password
        """

        self.assertTrue(check_password(password='password', encoded=self.user.password))
        updating_account(uid=self.uid_2.uid.hex, user_id=1, action='reset_password')
        self.user.refresh_from_db()
        self.assertTrue(check_password(password='new_password', encoded=self.user.password))
