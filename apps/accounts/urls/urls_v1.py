from rest_framework.routers import DefaultRouter

from ..views.views_v1 import AccountViewSetV1

router = DefaultRouter()

router.register("accounts", AccountViewSetV1, basename="accounts")

urlpatterns = router.urls
