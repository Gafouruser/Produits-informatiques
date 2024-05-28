# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('vulnerability_product/<str:product_cpe_name>/', views.vulnerability_product, name='vulnerability_product'),
]
