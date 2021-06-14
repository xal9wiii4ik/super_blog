from rest_framework.routers import SimpleRouter

from apps.posts.views import CategoryViewSet, PostModelViewSet

posts_router = SimpleRouter()
posts_router.register(prefix=r'categories', viewset=CategoryViewSet)
posts_router.register(prefix=r'posts', viewset=PostModelViewSet)

urlpatterns = posts_router.urls
