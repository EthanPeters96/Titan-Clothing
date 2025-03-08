from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Product
from django.db.models import Q

# Create your views here.


def all_products(request):
    """ A view to display all products, including sorting, search queries """

    products = Product.objects.all()
    query = None
    
    if request.GET and 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(
                request, "You didn't enter any search requirements!"
            )
            return redirect(reverse('products'))
        
        # Search in both name and description fields
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }
    
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to display individual products """

    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
    }

    return render(request, 'products/product_detail.html', context)

