import uuid
import colorlog
import logging

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from rest_framework.request import Request

from blog import settings
from apps.user_profile.models import Uid, Account

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(asctime)s] %(levelname)s- %(message)s'))

logger = colorlog.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def send_activation_email(request: Request, data: dict):
    """
    Sending activation email to user
    :return:
    """

    logger.info(msg='creating web url')
    uid_data = _create_unique_uid(user_id=data['id'])
    url = _current_ip_port(is_secure=request.is_secure(),
                           host=request.get_host(),
                           url=f'/api/account/activate_account/{uid_data["uid"]}/{uid_data["user_id"]}')
    logger.info(msg=f'sending activation email')
    # TODO move send email to celery
    send_mail(subject='Activation mail',
              message=f'Your activation link: \n {url}',
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[request.data['email']],
              fail_silently=False)
    logger.info(msg=f'Email has been send to {request.data["email"]}')


def activation_account(uid: str, user_id: int):
    """
    Activate user account
    """

    try:
        current_uid = Uid.objects.get(uid=uid, user_id=user_id)
        account = get_user_model().objects.get(pk=current_uid.user_id)
        account.is_active = True
        account.last_login = timezone.now()
        account.save()
        current_uid.delete()
        logger.info(f'Account with id:{account.pk} has been activate')
    except Uid.DoesNotExist as e:
        print(e)
        # TODO: add redirect to 404 page


def _create_unique_uid(user_id: int) -> dict:
    """
    Generating new uid and save in the db
    :param user_id:
    :return: dict with uid and user_id
    """

    uid = Uid.objects.create(uid=uuid.uuid1(), user_id=user_id)
    return {'uid': uid.uid.hex, 'user_id': user_id}


def _current_ip_port(is_secure: bool, host: str, url: str) -> str:
    """
    Creating web url with the current port and ip
    :param is_secure:
    :param host:
    :param url:
    :return:
    """

    protocol = 'https://' if is_secure else 'http://'
    web_url = protocol + host
    return web_url + url
