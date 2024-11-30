from django.shortcuts import redirect, render
from accounts.models import Cart, CartItems
from products.models import Product, SizeVariant
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError

# Create your views here.

def get_product(request, slug):
    try:
        product = Product.objects.get(slug = slug)
        context = {'product' : product}

        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            print(price)
        return render(request, 'product/product.html', context= context)
    
    except Product.DoesNotExist:
        # Product was not found for the given slug
        return HttpResponseNotFound(f"Product with slug '{slug}' not found.")

    except Exception as e:
        print(f"Error: {e}")
        return HttpResponseServerError("An error occurred while processing your request.")






