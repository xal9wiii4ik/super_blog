from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action

from apps.user_profile.models import Account
from apps.user_profile.serializers import AccountModelSerializer
from apps.user_profile.permmissions import IsAuthenticatedOrOwner
from apps.user_profile.services_views import send_activation_email, activation_account


class UserProfileModelViewSet(ModelViewSet):
    """
    Model View Set for model Account
    """

    queryset = Account.objects.all()
    serializer_class = AccountModelSerializer
    permission_classes = (IsAuthenticatedOrOwner,)
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs) -> Response:
        request.data['is_active'] = False
        response = super(UserProfileModelViewSet, self).create(request, *args, **kwargs)
        send_activation_email(request=request, data=response.data)
        return response

    @action(detail=False,
            methods=['GET'],
            permission_classes=[permissions.AllowAny],
            url_path=r'activate_account/(?P<uid>\w+)/(?P<user_id>\d+)')
    def activate_account(self, request, *args, **kwargs):
        activation_account(uid=str(kwargs['uid']), user_id=int(kwargs['user_id']))
        return Response(data={'ok': 'user has been activate successfully'}, status=status.HTTP_200_OK)
