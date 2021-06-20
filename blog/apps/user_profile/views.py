from rest_framework.viewsets import ModelViewSet

from apps.user_profile.models import Account
from apps.user_profile.serializers import AccountModelSerializer
from apps.user_profile.permmissions import IsAuthenticatedOrOwner


class UserProfileModelViewSet(ModelViewSet):
    """
    Model View Set for model Account
    """

    queryset = Account.objects.all()
    serializer_class = AccountModelSerializer
    permission_classes = (IsAuthenticatedOrOwner,)
