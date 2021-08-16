from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.user_profile.views import CustomTokenObtainPairView

from blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('apps.posts.urls', 'post'), namespace='post')),
    path('api/', include(('apps.user_profile.urls', 'user_profile'), namespace='user_profile')),
    path('token/', CustomTokenObtainPairView.as_view(), name='token')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
