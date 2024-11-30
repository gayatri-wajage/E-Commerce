from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import Profile
from products.models import *
from accounts.models import Cart, CartItems

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = email)

        if not user.exists():
            messages.warning(request, "Account not found")
            return HttpResponseRedirect(request.path_info)
        
        if not user[0].profile.is_emali_verified:
            messages.warning(request, "Your Account is not Verified")
            return HttpResponseRedirect(request.path_info)
        
        user = User.objects.create(username = email, email = email)

        if user:
            login(request, user)
            return redirect('/')

        messages.success(request,"Invalid Credentials")
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = email)

        if user.exists():
            messages.warning(request, "Email already exists")
            return HttpResponseRedirect(request.path_info)
        
        user = User.objects.create(username = email, first_name = first_name, last_name = last_name, email = email)
        user.set_password(password)
        user.save()

        messages.success(request,"An Email has been sent on your mail.")
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/register.html')


def activate_email(request, email_token):
    try :
        user = Profile.objects.get(email_token = email_token)
        user.is_emali_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid email Token')
    

def add_to_cart(request, uid):

    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if not logged in

    variant = request.GET.get('variant')

    product = Product.objects.get(uid = uid)
    user = request.user
    cart, _ = Cart.objects.get_or_create(user = user, is_paid =False)

    cart_item = CartItems.objects.create(cart = cart, product = product)

    if variant:
        variant =request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_item.size_variant =size_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()

    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   

def cart(request):
    cart_obj = None
    try:
        cart_obj = Cart.objects.get(user = request.user, is_paid =False)
    except Exception as e:
        print(e)
    if request.method == 'POST':
        Coupon = request.POST.get('coupon')
        Coupon_obj = Coupon.objects.filter(Coupon_code__icontains = Coupon)

        if not Coupon_obj.exists():
            messages.warning(request, "Invalid coupon.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

        if cart_obj.coupon:
            messages.warning(request, "Coupon Already Exists.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
        
        if cart_obj.get_cart_total() < Coupon_obj[0].minimum_amount:
            messages.warning(request, f"Amount should be greater than {Coupon_obj[0].minimum_amount}.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
        
        if Coupon_obj[0].is_expired:
            messages.warning(request, f"Coupon expired.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

        
        cart_obj.coupon = Coupon_obj[0]
        cart_obj.save()
        messages.warning(request, " coupon Applied  .")
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  




    context = {'cart' : cart_obj }        
    return render(request, 'accounts/cart.html', context)

def remove_coupon(request, cart_id):
     cart = Cart.objects.get(uid = cart_id)
     cart.coupon = None
     cart.save()
     messages.warning(request, f"Coupon removed.")
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))