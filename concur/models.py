from django.db import models


class Customer(models.Model):
    login = models.CharField(unique=True, max_length=255)
