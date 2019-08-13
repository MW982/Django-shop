from django.shortcuts import render

# Create your views here.
from product.models import Product


def homepage(request):
    context = {'Products': Product.objects.all}
    return render(request, 'product/home.html', context)


def detail(request, p_id):
    context = {'Product': Product.objects.get(id=p_id)}
    return render(request, 'product/item.html', context)
