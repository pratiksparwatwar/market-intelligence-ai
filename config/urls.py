import os
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import FileResponse
from django.conf import settings as django_settings


def service_worker(request):
    sw_path = os.path.join(django_settings.BASE_DIR, 'static', 'sw.js')
    response = FileResponse(open(sw_path, 'rb'), content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache'
    return response


def manifest(request):
    path_ = os.path.join(django_settings.BASE_DIR, 'static', 'manifest.json')
    response = FileResponse(open(path_, 'rb'), content_type='application/manifest+json')
    response['Cache-Control'] = 'no-cache'
    return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sw.js', service_worker),
    path('manifest.json', manifest),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('', include('themes.urls')),
    path('news/', include('news.urls')),
]
