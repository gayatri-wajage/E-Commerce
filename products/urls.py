from django.urls import path

from products import views
from . import views




urlpatterns = [
    path('<slug>/', views.get_product, name='get_product'),
    
]