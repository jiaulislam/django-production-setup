from rest_framework.routers import DefaultRouter

from ..views.views_v2 import AccountViewSetV2

router = DefaultRouter()

router.register("accounts", AccountViewSetV2, basename="accounts")

urlpatterns = router.urls
