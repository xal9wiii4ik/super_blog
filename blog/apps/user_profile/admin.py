from django.contrib import admin

from apps.user_profile.models import Account, Uid


@admin.register(Account)
class AccountModelAdmin(admin.ModelAdmin):
    """
    Display table account on admin panel
    """

    pass


@admin.register(Uid)
class UidModelAdmin(admin.ModelAdmin):
    """
    Display table Uid on admin panel
    """

    pass
