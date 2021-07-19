import uuid
import colorlog
import logging

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from rest_framework.request import Request

from blog import settings
from apps.user_profile.models import Uid

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(asctime)s] %(levelname)s- %(message)s')
)
logger = colorlog.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def send_updating_email(request: Request, data: dict, action: str, email: str = None, updated_data: str = None):
    """
    Sending email for updating account or activate and etc
    """

    logger.info(msg=f'creating web url for {action}')
    uid_data = _create_unique_uid(user_id=data['id'],
                                  updated_data=updated_data)
    url = _current_ip_port(is_secure=request.is_secure(),
                           host=request.get_host(),
                           url=f'/api/account/{action}/{uid_data["uid"]}/{uid_data["user_id"]}')
    logger.info(msg=f'sending email with {action}')
    message = f'Your new email: {email}' if email is not None else ''
    message += f'New password will be: {data["password"]}. ' \
               f'Dont forgot again' if action == 'reset_password_confirm' else ''
    # TODO move send email to celery
    send_mail(subject=f'{action} email',
              message=f'Your {action} link: \n {url}\n' + message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[data['email'] if email is not None else request.data.get('email')],
              fail_silently=False)
    logger.info(msg=f'Email has been send to {data["email"] if email is not None else request.data.get("email")}')


def updating_account(uid: str, user_id: int, action: str):
    """
    Func for activate account or updating fields who need confirmation
    """

    try:
        current_uid = Uid.objects.get(uid=uid, user_id=user_id)
        account = get_user_model().objects.get(pk=current_uid.user_id)
        account.email = current_uid.updated_data if action == 'update_account' else account.email
        account.password = current_uid.updated_data if action == 'reset_password' else account.password
        account.is_active = True
        account.last_login = timezone.now()
        account.save()
        current_uid.delete()
        logger.info(f'Account with id:{account.pk} has been updated')
    except Exception as e:
        print(e)
        # TODO: add redirect to 404 page


def _create_unique_uid(user_id: int, updated_data: str = None) -> dict:
    """
    Generating new uid and save in the db
    :param user_id:
    :return: dict with uid and user_id
    """

    uid = Uid.objects.create(uid=uuid.uuid1(), user_id=user_id)
    if updated_data is not None:
        uid.updated_data = updated_data
        uid.save()
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
