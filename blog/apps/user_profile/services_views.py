import uuid
import colorlog
import logging

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.request import Request

from apps.user_profile.tasks.tasks import send_email_task
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
    logger.info(f'Move send email with action: {action} to celery task')
    request.data.pop('image', None)
    send_email_task.delay(data=data, action=action, url=url, request_data=request.data, email=email)


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
