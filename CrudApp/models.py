from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    qtty = models.CharField(max_length=30, blank=False, null=False)
    size = models.CharField(max_length=25, blank=False, null=False)
    price = models.CharField(max_length=20, blank=False, null=False)


def __str__(self):
    return self.name