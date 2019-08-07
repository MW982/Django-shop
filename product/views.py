from django.shortcuts import render

# Create your views here.
from product.models import Product


def homepage(request):
    return render(request, 'product/home.html', {'Products': Product.objects.all})

def detail(request, p_id):
    return render(request, 'product/item.html', {'Product': Product.objects.get(id=p_id)})
