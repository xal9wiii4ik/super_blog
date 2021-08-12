from rest_framework.exceptions import ValidationError

from apps.user_profile.models import Account


def validate_email(email: str, action: str) -> int or None:
    """
    Checking email in exists users
    """

    try:
        account = Account.objects.get(email=email)
        if action == 'create_user':
            raise ValidationError('email exist')
        return account.id
    except Account.DoesNotExist as e:
        if action == 'reset_password':
            raise ValidationError('user with this email not found')


def validate_passwords(password: str, repeat_password: str) -> None:
    """
    Checking if password is similar repeat password
    """

    if password != repeat_password:
        raise ValidationError('Password is not similar repeat password')
