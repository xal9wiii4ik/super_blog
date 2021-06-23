import typing as tp

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.user_profile.models import Account
from apps.user_profile.serializers_services import validate_email


class AccountModelSerializer(serializers.ModelSerializer):
    """
    Model serializer for model Account
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('password', 'username',
                  'first_name',
                  'last_name',
                  'email',
                  'image',
                  'gender',
                  'phone',
                  'id',
                  'is_active')
        # exclude = ('last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions', 'password')

    def validate(self, attrs) -> tp.Any:
        """
        Validate data of serializer
        """

        if attrs.get('password') is not None:
            validate_password(password=attrs['password'])
            attrs['password'] = make_password(password=attrs['password'])
        if attrs.get('email') is not None:
            validate_email(email=attrs['email'])
        data = super(AccountModelSerializer, self).validate(attrs)
        return data
