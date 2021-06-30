import typing as tp

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user_profile.models import Account
from apps.user_profile.serializers_services import validate_email, validate_passwords


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Custom token serializer """

    def to_internal_value(self, data: tp.Any):
        data['username'] = Account.objects.get(email=data['email']).username if data.get('email') is not None \
            else data.get('username')
        return super(CustomTokenObtainPairSerializer, self).to_internal_value(data)

    def validate(self, attrs: tp.Any):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data['id'] = Account.objects.get(username=attrs['username']).id
        return data


class AccountModelSerializer(serializers.ModelSerializer):
    """
    Model serializer for model Account
    """

    class Meta:
        model = Account
        fields = ('password', 'username', 'first_name', 'last_name',
                  'email', 'image', 'gender', 'phone', 'id', 'is_active')

    password = serializers.CharField(write_only=True)

    # TODO move mb password from validate to validate_password and email

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
