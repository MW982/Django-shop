from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('addcart<int:cart_id>', views.addCart, name='addCart'),
    path('buyPage', views.buyPage, name='buyPage')
]
