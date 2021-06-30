import typing as tp
from abc import ABC

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.user_profile.models import Account
from apps.user_profile.serializers_services import validate_email, validate_passwords


class AccountModelSerializer(serializers.ModelSerializer):
    """
    Model serializer for model Account
    """

    password = serializers.CharField(write_only=True)
    # TODO move mb password from validate to validate_password and email

    class Meta:
        model = Account
        fields = ('password', 'username', 'first_name', 'last_name',
                  'email', 'image', 'gender', 'phone', 'id', 'is_active')

    def validate(self, attrs) -> tp.Any:
        """
        Validate data of serializer
        """

        if attrs.get('password') is not None:
            validate_password(password=attrs['password'])
            # TODO add field Repeat_password
            attrs['password'] = make_password(password=attrs['password'])
        if attrs.get('email') is not None:
            validate_email(email=attrs['email'], action='create_user')
        data = super(AccountModelSerializer, self).validate(attrs)
        return data


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset password serializer
    """

    email = serializers.EmailField(max_length=60, required=True)
    password = serializers.CharField(max_length=60, required=True)
    repeat_password = serializers.CharField(max_length=60, required=True)
    id = serializers.IntegerField(read_only=True)

    @staticmethod
    def validate_password(value: str) -> str:
        """Validation password"""

        validate_password(password=value)
        return value

    def validate(self, attrs) -> tp.Any:
        """
        Validate data of serializer
        """

        data = super(ResetPasswordSerializer, self).validate(attrs)
        validate_passwords(password=attrs['password'], repeat_password=attrs['repeat_password'])
        user_id = validate_email(email=attrs['email'], action='reset_password')
        data['id'] = user_id
        data['repeat_password'] = make_password(password=attrs['repeat_password'])
        return data
