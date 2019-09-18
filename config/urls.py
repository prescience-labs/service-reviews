from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Reviews Service')

# Admin site settings
admin.site.site_title   = settings.ADMIN_SITE['site_title']
admin.site.site_header  = settings.ADMIN_SITE['site_header']
admin.site.index_title  = settings.ADMIN_SITE['index_title']

urlpatterns = [
    path('', schema_view),
    path('v1', include('v1.urls')),
    path('admin/', admin.site.urls),
]
