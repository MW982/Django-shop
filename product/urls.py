from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("", views.homepage_view, name="homepage"),
    path("<int:p_id>", views.detail_view, name="detail"),
]
