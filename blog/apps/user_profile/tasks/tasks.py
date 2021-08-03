import colorlog
import logging
import requests
import json
import typing as tp

from celery import shared_task
from django.core.files.uploadedfile import InMemoryUploadedFile

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(asctime)s] %(levelname)s- %(message)s')
)
logger = colorlog.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@shared_task
def send_email_task(data: dict, action: str, url: str, request_data: dict, email: str = None) -> None:
    """ Sending mail with action
    Args:
        data: dict with account data
        action: action(update account etc.)
        url: url
        request_data: dict with request data
        email: email
    """

    from django.core.mail import send_mail
    from blog import settings

    logger.info(msg=f'sending email with {action}')
    message = f'Your new email: {email}' if email is not None else ''
    message += f'New password will be: {data["password"]}. ' \
               f'Dont forgot again' if action == 'reset_password_confirm' else ''
    send_mail(subject=f'{action} email',
              message=f'Your {action} link: \n {url}\n' + message,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[data['email'] if email is not None else request_data.get('email')],
              fail_silently=False)
    logger.info(msg=f'Email has been send to {data["email"] if email is not None else request_data.get("email")}')


@shared_task
def updating_account_task(uid: str, user_id: int, action: str) -> dict:
    """ Func for activate account or updating fields who need confirmation
    Args:
        uid: uid,
        user_id: user_id,
        action: action
    Returns:
        dict with success message
    """

    from apps.user_profile.models import Uid
    from django.contrib.auth import get_user_model
    from django.utils import timezone

    try:
        current_uid = Uid.objects.get(uid=uid, user_id=user_id)
        account = get_user_model().objects.get(pk=current_uid.user_id)
    except Exception as e:
        logger.exception(f'Error with {action} in func updating_account')
        return {'error': 'There is no such uid'}
    account.email = current_uid.updated_data if action == 'update_account' else account.email
    account.password = current_uid.updated_data if action == 'reset_password' else account.password
    account.is_active = True
    account.last_login = timezone.now()
    account.save()
    current_uid.delete()
    logger.info(f'Account with id:{account.pk} has been updated')
    return {'ok': 'Account has been updated successfully'}


@shared_task
def send_telegram_message(message: str,
                          group_type: str = None,
                          chat_id: str = None,
                          files: tp.Union[tp.List[InMemoryUploadedFile]] = None) -> None:
    """ Sending telegram message to user chat or to group with success or error
    Args:
        chat_id: chat id
        message: telegram message
        group_type: success or error
        files: list with files
    """

    from apps.user_profile.models import TelegramGroup
    from blog.settings import BOT_TOKEN

    message_url = f'https://api.telegram.org/bot{BOT_TOKEN}' \
                  f'/sendMessage?chat_id={chat_id}&text={message}'
    if group_type is not None:
        chats = TelegramGroup.objects.filter(group_type=group_type)
        for chat in chats:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}' \
                  f'/sendMessage?chat_id={chat.group_id}&text={message}'
            response = requests.post(url=url)
    else:
        response = requests.post(url=message_url)
        image_url = f'https://api.telegram.org/bot{BOT_TOKEN}' \
                    f'/sendPhoto?chat_id={chat_id}'
        if files is not None:
            for file in files:
                data = {'files': {'photo': file.open()}}
                response = requests.post(url=image_url, **data)

    if response.status_code != 200:
        print(response.json())
        description = json.loads(response.content)
        logging.info(f'Bad request(send message to user in telegram) {description["description"]}')


@shared_task
def update_subscribers(subscribers: tp.List[int], pk: int) -> tp.List[int]:
    """ Update subscribers getting dict with data from request and return new dict
    Args:
        subscribers: list with subscribers
        pk: UserSubscriber pk
    Returns:
        Dict with new data
    """

    from apps.user_profile.models import UserSubscriber

    try:
        user_subscribers = UserSubscriber.objects.get(id=pk)
        for user_subscriber in user_subscribers.subscribers.all():
            subscribers.append(user_subscriber.pk)
        if user_subscribers.owner.pk in subscribers:
            subscribers.remove(user_subscribers.owner.pk)
        if user_subscribers.owner.telegram_chat_id is not None \
                and len(set(subscribers)) > len(user_subscribers.subscribers.all()):
            send_telegram_message.delay(message='Congratulations you have 1 new subscriber',
                                        chat_id=user_subscribers.owner.telegram_chat_id)
        return subscribers
    except Exception as e:
        logger.warning(msg=f'Error in func update_subscribers {str(e)}')
        return []
