from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("addcart<int:cart_id>", views.add_cart_view, name="addCart"),
    path("buyPage", views.buy_page_view, name="buyPage"),
]
