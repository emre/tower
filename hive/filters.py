from django_filters import rest_framework as filters
from django_filters.rest_framework.backends import DjangoFilterBackend
from .models import Account
from rest_framework.filters import OrderingFilter


class TowerFilterBackend(DjangoFilterBackend):
    def get_schema_fields(self, view):
        if view.action not in ["list"]:
            return []
        return super().get_schema_fields(view)


class TowerOrderingFilter(OrderingFilter):
    def get_schema_fields(self, view):
        if view.action not in ["list"]:
            return []
        return super().get_schema_fields(view)


class AccountFilter(filters.FilterSet):
    min_rep = filters.NumberFilter(
        field_name="reputation",
        lookup_expr="gte",
        label="Minimum reputation"
    )
    max_rep = filters.NumberFilter(field_name="reputation", lookup_expr='lte')

    min_vote_weight = filters.NumberFilter(field_name="vote_weight",
                                           lookup_expr='gte')
    max_vote_weight = filters.NumberFilter(field_name="vote_weight",
                                           lookup_expr='lte')

    min_following = filters.NumberFilter(field_name="following",
                                         lookup_expr='gte')
    max_following = filters.NumberFilter(field_name="following",
                                         lookup_expr='lte')

    min_followers = filters.NumberFilter(field_name="followers",
                                         lookup_expr='gte')
    max_followers = filters.NumberFilter(field_name="followers",
                                         lookup_expr='lte')

    min_active_at = filters.NumberFilter(field_name="active_at",
                                         lookup_expr='gte')
    max_active_at = filters.NumberFilter(field_name="active_at",
                                         lookup_expr='lte')

    min_created_at = filters.NumberFilter(field_name="created_at",
                                          lookup_expr='gte')
    max_created_at = filters.NumberFilter(field_name="created_at",
                                          lookup_expr='lte')

    location__contains = filters.CharFilter(field_name="location",
                                            lookup_expr="contains")

    name__contains = filters.CharFilter(field_name="name",
                                        lookup_expr="contains")

    class Meta:
        model = Account
        fields = '__all__'


class PostFilter(filters.FilterSet):
    pass
