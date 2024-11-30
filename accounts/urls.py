#from django.contrib import admin
from django.urls import path

from accounts import views




urlpatterns = [
    #path('admin/', admin.site.urls),
    path('login/', views.login, name='login.html'),
    path('register/', views.register, name='register.html'),
    path('activate/<email_token>/', views.activate_email, name = 'activate_email'),
    path('cart/', views.cart, name = 'cart.html'),
    path('add-to-cart/<uid>/', views.add_to_cart, name="add_to_cart"),
    path('remove-cart/<cart_item_uid>/', views.remove_cart, name = 'remove_cart'),
     path('remove-coupon/<cart_id>/', views.remove_coupon, name='remove_coupon'),
]