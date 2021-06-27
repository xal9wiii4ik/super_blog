from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action

from apps.user_profile.models import Account
from apps.user_profile.serializers import AccountModelSerializer
from apps.user_profile.permmissions import IsAuthenticatedOrOwner
from apps.user_profile.services_views import send_activation_email, updating_account, send_updating_email
    # update_email, activation_account


class UserProfileModelViewSet(ModelViewSet):
    """
    Model View Set for model Account
    """

    queryset = Account.objects.all()
    serializer_class = AccountModelSerializer
    permission_classes = (IsAuthenticatedOrOwner,)
    parser_classes = (MultiPartParser,)
    # TODO update tests

    def partial_update(self, request, *args, **kwargs) -> Response:
        request.data._mutable = True
        if request.data.get('email') is not None:
            email = request.data.pop('email')
            response = super(UserProfileModelViewSet, self).partial_update(request, *args, **kwargs)
            send_updating_email(request=request, data=response.data, action='update_account', email=email[0])
        response = super(UserProfileModelViewSet, self).partial_update(request, *args, **kwargs)
        return Response(data=response.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs) -> Response:
        request.data['is_active'] = False
        response = super(UserProfileModelViewSet, self).create(request, *args, **kwargs)
        # send_activation_email(request=request, data=response.data)
        send_updating_email(request=request, data=response.data, action='activate_account')
        return response

    @action(detail=False,
            methods=['GET'],
            permission_classes=[permissions.AllowAny],
            url_path=r'activate_account/(?P<uid>\w+)/(?P<user_id>\d+)')
    def activate_account(self, request, *args, **kwargs) -> Response:
        """
        Url for activate account
        """

        updating_account(uid=str(kwargs['uid']), user_id=int(kwargs['user_id']))
        return Response(data={'ok': 'email has been updated successfully'}, status=status.HTTP_200_OK)

    @action(detail=False,
            methods=['GET'],
            permission_classes=[permissions.AllowAny],
            url_path=r'update_account/(?P<uid>\w+)/(?P<user_id>\d+)')
    def update_account(self, request, *args, **kwargs) -> Response:
        """
        Url for update fields in account(email)
        """

        updating_account(uid=str(kwargs['uid']), user_id=int(kwargs['user_id']))
        return Response(data={'ok': 'user has been activate successfully'}, status=status.HTTP_200_OK)
