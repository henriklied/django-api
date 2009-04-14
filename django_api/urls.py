from django.conf.urls.defaults import *

from django_api import views


urlpatterns = patterns('',    
    
    url(r'^(?P<api_name>.+)$', views.api_request, name='django_api_views_api_request'),
    url(r'^$', views.api_doc, name="django_api_views_api_doc"),
)
