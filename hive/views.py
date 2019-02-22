from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import AccountFilter, TowerFilterBackend, TowerOrderingFilter
from .models import Account, Block, Post, PostCache, State
from .pagination import TowerLimitedPagination
from .serializers import (
    AccountSerializer, BlockSerializer, PostCacheSerializer,
    PostSerializer, HiveStateSerializer,
    AccountFollowerSerializer, AccountFollowingSerializer,
    AccountMuterSerializer, AccountMutingSerializer
)


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

    @action(detail=True, methods=["get"])
    def followers(self, *args, **kwargs):
        """
        Returns the related account's active followers.
        """
        serializer = AccountFollowerSerializer(self.get_object())
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def following(self, *args, **kwargs):
        """
        Returns the related account's active followings.
        """
        serializer = AccountFollowingSerializer(self.get_object())
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def muters(self, *args, **kwargs):
        """
        Returns the related account's active muters
        """
        serializer = AccountMuterSerializer(self.get_object())
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def muting(self, *args, **kwargs):
        """
        Returns the related account's active mutings.
        """
        serializer = AccountMutingSerializer(self.get_object())
        return Response(serializer.data)


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

    def _get_by_author_permlink(self, **kwargs):
        try:
            try:
                post_cache = PostCache.objects.get(
                    author=kwargs["author"],
                    permlink=kwargs["permlink"],
                )
            except KeyError as e:
                post_cache = PostCache.objects.get(
                    pk=kwargs.get("pk"),
                )
        except PostCache.DoesNotExist:
            return None

        return post_cache

    def retrieve(self, request, *args, **kwargs):
        post_cache = self._get_by_author_permlink(**kwargs)
        return Response(PostCacheSerializer(post_cache).data)


    @action(detail=True, methods=["get"])
    def votes(self, *args, **kwargs):
        """Returns the vote(r) information of the post.
        """
        response = []
        obj = self._get_by_author_permlink(**kwargs)
        if not obj.votes:
            return response
        votes = obj.votes.split("\n")
        for row in votes:
            # ignore the reputation
            # https://github.com/steemit/hivemind/issues/175
            voter, rshares, percent, _ = row.split(",")
            response.append(
                {"voter": voter, "rshares": rshares, "percent": percent})
        return Response(response)



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
