
from django.contrib import admin
from django.urls import path, include

from hive.urls import router
from hive.views import StateView
from hive.views import PostCacheViewSet
from rest_framework.documentation import include_docs_urls

post_cache_detail = PostCacheViewSet.as_view({
    'get': 'retrieve',
})

post_cache_list = PostCacheViewSet.as_view({
    'get': 'list',
})

post_cache_detail_votes = PostCacheViewSet.as_view({
    'get': 'votes',
})

post_cache_detail_reblogs = PostCacheViewSet.as_view({
    'get': 'reblogs',
})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/state/', StateView.as_view(), name="state"),
    path(
        'api/v1/post_cache/',
        post_cache_list,
        name="post-cache-list"),
    path(
        'api/v1/post_cache/<str:author>/<str:permlink>/',
        post_cache_detail,
        name="post-cache-detail"),
    path(
        'api/v1/post_cache/<str:author>/<str:permlink>/votes/',
        post_cache_detail_votes,
        name="post-cache-detail-votes"),
    path(
        'api/v1/post_cache/<str:author>/<str:permlink>/reblogs/',
        post_cache_detail_reblogs,
        name="post-cache-detail-reblogs"),
    path('', include_docs_urls(title='Tower API')),
]
