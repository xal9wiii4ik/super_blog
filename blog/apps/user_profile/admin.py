from django.contrib import admin

from apps.user_profile.models import Account, Uid, TelegramGroup


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


@admin.register(TelegramGroup)
class TelegramGroupModelAdmin(admin.ModelAdmin):
    """
    Display table TelegramGroup on admin panel
    """

    pass
