from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets

from .filters import AccountFilter, TowerFilterBackend, TowerOrderingFilter
from .models import Account, Block, Post, PostCache
from .pagination import TowerLimitedPagination
from .serializers import (
    AccountSerializer, BlockSerializer, PostCacheSerializer,
    PostSerializer)


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the given account by name.

    list:
    Return a list of all the existing steem accounts.
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'name'
    filter_backends = (TowerFilterBackend, TowerOrderingFilter)
    ordering_fields = (
        'vote_weight',
        'proxy_weight',
        'reputation',
        'post_count',
        'followers',
        'following',
        'proxy_weight',
    )
    search_fields = ('name',)
    filter_fields = ('location', 'name', 'reputation')
    filterset_class = AccountFilter



class BlockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
    Return the block details by block number.

    list:
    Return a list of all blocks in the blockchain.
    """
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    filter_backends = (TowerOrderingFilter,)
    ordering_fields = ('txs', 'ops')


class PostCacheViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostCache.objects.all()
    serializer_class = PostCacheSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('author', 'permlink')
    pagination_class = TowerLimitedPagination


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('category', 'author', 'is_deleted')
