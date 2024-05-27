from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product

def product_list(request):
    query = request.GET.get('q')
    if query:
        products_list = Product.objects.filter(name__icontains=query)
    else:
        products_list = Product.objects.all()
    
    paginator = Paginator(products_list, 50)  # 50 éléments par page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/product_list.html', {'page_obj': page_obj, 'query': query})
