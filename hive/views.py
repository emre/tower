from django.http import Http404
from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import AccountFilter, TowerFilterBackend, TowerOrderingFilter
from .models import Account, Block, Post, PostCache, State, Reblog, PostTag
from .pagination import TowerLimitedPagination
from .serializers import (
    AccountSerializer, BlockSerializer, PostCacheSerializer,
    PostSerializer, HiveStateSerializer,
    AccountFollowerSerializer, AccountFollowingSerializer,
    AccountMuterSerializer, AccountMutingSerializer,
    ReblogSerializer
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

    @action(detail=True, methods=["get"])
    def reblogs(self, *args, **kwargs):
        """
        Returns the reblogs of the user.
        """
        obj = self.get_object()
        reblogs = Reblog.objects.filter(account=obj.name).order_by(
            "-created_at").values(
            'post__author', 'post__permlink', 'created_at')
        page = self.paginate_queryset(reblogs)
        if page is not None:
            serializer = ReblogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
        if not post_cache:
            raise Http404
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

    @action(detail=True, methods=["get"])
    def reblogs(self, *args, **kwargs):
        """Returns the rebloggers of the post.
        """
        obj = self._get_by_author_permlink(**kwargs)
        reblogs = Reblog.objects.filter(post=obj.post).order_by("-created_at").values_list(
            'account', 'created_at')
        return Response([{
            "author": reblog[0],
            "reblogged_at": reblog[1],
        } for reblog in reblogs])

    @action(detail=False, methods=["get", ])
    def filter_by_tags(self, *args, **kwargs):
        """Filter the result set by tags. Example: ?[]exact=python&[]
        exact=programming&[]exact=utopian-io
        """
        exact_matches = self.request.query_params.getlist("[]exact", [])
        if not len(exact_matches):
            raise Http404
        with connection.cursor() as cursor:
            subqueries = []
            for _ in exact_matches:
                subqueries.append("SELECT post_id " \
                           "FROM hive_post_tags " \
                           "WHERE tag = %s")
            subquery = " INTERSECT ".join(subqueries)
            subquery = "(%s)" % subquery
            cursor.execute(subquery, exact_matches)
            post_ids = [p[0] for p in cursor.fetchall()]

        post_cache_objects = PostCache.objects.filter(pk__in=post_ids).order_by(
            "-created_at")
        page = self.paginate_queryset(post_cache_objects)
        if page is not None:
            serializer = PostCacheSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('category', 'author', 'is_deleted')

    def _get_by_author_permlink(self, **kwargs):
        try:
            try:
                post = Post.objects.get(
                    author=kwargs["author"],
                    permlink=kwargs["permlink"],
                )
            except KeyError as e:
                post = Post.objects.get(
                    pk=kwargs.get("pk"),
                )
        except PostCache.DoesNotExist:
            return None

        return post

    def retrieve(self, request, *args, **kwargs):
        post = self._get_by_author_permlink(**kwargs)
        if not post:
            raise Http404
        return Response(PostSerializer(post).data)


class StateView(APIView):
    """
    Return the current HEAD block processed by Tower/Hivemind.
    """

    def get(self, request, format=None):
        state = State.objects.last()
        serializer = HiveStateSerializer(state)
        return Response(serializer.data)
