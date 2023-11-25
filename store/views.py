from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from store.models import *
from carts.models import *
from carts.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.

def store(request,category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products,10)
        page=request.GET.get('page')
        paged_products  = paginator.get_page(page)
        product_count = products.count()
    else: 
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,10)
        page=request.GET.get('page')
        paged_products  = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products':paged_products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        incart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
   
        
    except Exception as e:
        raise e
    
    context = {
        'single_product':single_product,
        'incart':incart,
    }
        
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    
    context = {
        'products':products,
        'product_count':product_count,
    }
        
    return render(request,'store/store.html',context)