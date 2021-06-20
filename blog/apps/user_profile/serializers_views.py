from rest_framework.exceptions import ValidationError

from apps.user_profile.models import Account


def validate_email(email: str) -> None:
    """
    Check email in exists users
    :param email:
    :return:
    """

    try:
        Account.objects.get(email=email)
        raise ValidationError('email exist')
    except Account.DoesNotExist as e:
        pass
