
from django.contrib import admin
from django.urls import path, include

from hive.urls import router
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/docs/', include_docs_urls(title='Tower API')),
]
