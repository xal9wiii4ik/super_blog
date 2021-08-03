from rest_framework.routers import SimpleRouter

from apps.user_profile.views import UserProfileModelViewSet, UserSubscriberModelViewSet

posts_router = SimpleRouter()
posts_router.register(prefix=r'account', viewset=UserProfileModelViewSet)
posts_router.register(prefix=r'subscriber', viewset=UserSubscriberModelViewSet)

urlpatterns = posts_router.urls
