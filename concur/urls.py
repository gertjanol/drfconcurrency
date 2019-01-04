from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from concur.views import CustomerViewset

router = DefaultRouter()
router.register('customer', CustomerViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
]
