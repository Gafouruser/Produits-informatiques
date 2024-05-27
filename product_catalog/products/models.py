# products/models.py
from django.db import models
from .enums import Category

class Product(models.Model):
    name = models.CharField(max_length=255)
    vendor = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(choices=[(category.value, category.name) for category in Category], max_length=30)
    version = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    cpe_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name