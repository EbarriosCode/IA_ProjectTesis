from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),    
    url(r'^$', views.Main), 
    url(r'^Deteccion/$', views.Deteccion),     
    url(r'^Enfermedades/$', views.Enfermedades),
     url(r'^testAjax/$', views.TestAjax),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)