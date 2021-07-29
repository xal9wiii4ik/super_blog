from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.posts.views import CategoryViewSet, PostModelViewSet, PostFilters

posts_router = SimpleRouter()
posts_router.register(prefix=r'categories', viewset=CategoryViewSet)
posts_router.register(prefix=r'posts', viewset=PostModelViewSet)

urlpatterns = [
    path('filters/', PostFilters.as_view(), name='get_filters'),
]


urlpatterns += posts_router.urls
