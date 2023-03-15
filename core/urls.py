from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from calendar_manager.views import HomePageView

urlpatterns = [
    #Adding social auth path
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('', include('accounts.urls')),
    path('calendar/', include('calendar_manager.urls')),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
