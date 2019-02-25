from rest_framework import routers

from .views import (
    AccountViewSet, BlockViewSet
)


router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet, base_name='accounts')
router.register(r'blocks', BlockViewSet, base_name='blocks')
