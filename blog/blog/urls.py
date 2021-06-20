from rest_framework_simplejwt.views import TokenObtainPairView

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('apps.posts.urls', 'post'), namespace='post')),
    path('api/', include(('apps.user_profile.urls', 'post'), namespace='user_profile')),
    path('token/', TokenObtainPairView.as_view(), name='token'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
