from rest_framework.routers import SimpleRouter

from apps.user_profile.views import UserProfileModelViewSet

posts_router = SimpleRouter()
posts_router.register(prefix=r'account', viewset=UserProfileModelViewSet)

urlpatterns = posts_router.urls
