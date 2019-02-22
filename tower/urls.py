
from django.contrib import admin
from django.urls import path, include

from hive.urls import router
from hive.views import StateView
from hive.views import PostCacheViewSet
from rest_framework.documentation import include_docs_urls

post_cache_detail = PostCacheViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/state/', StateView.as_view(), name="state"),
    path(
        'api/v1/post_cache/<str:author>/<str:permlink>/',
        post_cache_detail,
        name="post-cache-detail"),
    path('', include_docs_urls(title='Tower API')),
]
