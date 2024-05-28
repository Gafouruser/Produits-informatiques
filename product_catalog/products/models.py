# products/models.py
from django.db import models
from .enums import Category

class Vulnerability(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    vendor = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(choices=[(category.value, category.name) for category in Category], max_length=30)
    version = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    cpe_name = models.CharField(max_length=255, blank=True, null=True)
    vulnerability = models.ManyToManyField(Vulnerability, related_name = 'cve_product_list')

    def __str__(self):
        return self.name
