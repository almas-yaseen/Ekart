from django.shortcuts import render,redirect 
from django.http import HttpResponse
from store.models import Product 
from carts.models import CartItem,Cart
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart 
        
    

def add_cart(request,product_id):
    if request.method=="POST":
        color=request.POST['color']
        size = request.POST['size']
        print(color,size)
    product = Product.objects.get(id=product_id) #get the product
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
            
        )
    cart.save()
        
        
    try:
            cart_item = CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity +=1 #cart item quantity  
            cart_item.save()
        
    except  CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                
            )
            cart_item.save()
    return redirect('cart')

def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')
    
    
    
    
        



    



def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cartitem in cart_items:
            total += (cartitem.product.price*cartitem.quantity)
            quantity += cartitem.quantity
        tax = (2 *total)/100
        grand_total = total+tax
    
    except ObjectDoesNotExist:
        
        pass  #just ignore
    
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'grand_total':grand_total,
        'tax':tax,
        
    }
        
            
            
    return render(request,'store/cart.html',context)
