from django.contrib import admin

from apps.user_profile.models import Account


@admin.register(Account)
class AccountModelAdmin(admin.ModelAdmin):
    """
    Display table account on admin panel
    """

    pass
