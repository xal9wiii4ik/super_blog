import typing as tp

from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer

from apps.user_profile.models import Account
from apps.user_profile.serializers_views import validate_email


class AccountModelSerializer(ModelSerializer):
    """
    Model serializer for model Account
    """

    class Meta:
        model = Account
        fields = '__all__'

    def validate(self, attrs) -> tp.Any:
        """
        Validate data of serializer
        """

        if attrs.get('password') is not None:
            validate_password(password=attrs['password'])
        if attrs.get('email') is not None:
            validate_email(email=attrs['email'])
        data = super(AccountModelSerializer, self).validate(attrs)
        return data
