from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import AccountFilter, TowerFilterBackend, TowerOrderingFilter
from .models import Account, Block, Post, PostCache, State
from .pagination import TowerLimitedPagination
from .serializers import (
    AccountSerializer, BlockSerializer, PostCacheSerializer,
    PostSerializer, HiveStateSerializer)
from django.http import Http404



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
    lookup_value_regex = '[^/]+'
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
    """
    retrieve:
    Return the post_cache object by id.

    list:
    Return a list of all blocks in the blockchain.
    """
    queryset = PostCache.objects.all()
    serializer_class = PostCacheSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('author', 'permlink')
    pagination_class = TowerLimitedPagination
    lookup_fields = ('author', 'permlink')

    def retrieve(self, request, *args, **kwargs):
        try:
            try:
                pk = int(kwargs.get("pk"))
                post_cache = PostCache.objects.get(pk=pk)
            except ValueError as e:
                # fallback to {uuid}
                post_cache = PostCache.objects.get(
                    author=kwargs.get("pk"),
                    permlink=self.request.query_params.get("permlink"),
                )
        except PostCache.DoesNotExist:
            raise Http404

        return Response(PostCacheSerializer(post_cache).data)



class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('category', 'author', 'is_deleted')

    def retrieve(self, request, *args, **kwargs):
        try:
            try:
                pk = int(kwargs.get("pk"))
                post = Post.objects.get(pk=pk)
            except ValueError as e:
                # fallback to {uuid}
                post = Post.objects.get(
                    author=kwargs.get("pk"),
                    permlink=self.request.query_params.get("permlink"),
                )
        except PostCache.DoesNotExist:
            raise Http404

        return Response(Post(post).data)


class StateView(APIView):
    """
    Return the current HEAD block processed by Tower/Hivemind.
    """
    def get(self, request, format=None):
        state = State.objects.last()
        serializer = HiveStateSerializer(state)
        return Response(serializer.data)