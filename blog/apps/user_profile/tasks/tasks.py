import colorlog
import logging

from celery import shared_task

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
    """
    Func for activate account or updating fields who need confirmation
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
