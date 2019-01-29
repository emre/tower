
from django.contrib import admin
from django.urls import path, include

from hive.urls import router
from hive.views import StateView
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/state/', StateView.as_view(), name="state"),
    path('', include_docs_urls(title='Tower API')),
]
