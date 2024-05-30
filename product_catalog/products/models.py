# products/models.py
from django.db import models
from .enums import Category


class Product(models.Model):
    vendor = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(choices=[(category.value, category.name) for category in Category], max_length=30)
    version = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    cpe_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.cpe_name


class Vulnerability(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

