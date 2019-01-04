import time

from django.db import transaction
from rest_framework.viewsets import ModelViewSet

from concur.models import Customer
from concur.serializers import CustomerSerializer


class CustomerViewset(ModelViewSet):
    queryset = Customer.objects
    serializer_class = CustomerSerializer

    # @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super(CustomerViewset, self).create(request, *args, **kwargs)

    def perform_create(self, serializer, **extra_kwargs):
        time.sleep(0.5)
        return serializer.save(**extra_kwargs)
