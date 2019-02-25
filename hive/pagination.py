from rest_framework.pagination import LimitOffsetPagination


class TowerPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


class TowerLimitedPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10


