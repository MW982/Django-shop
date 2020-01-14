# import numpy as np
# import matplotlib.pyplot as plt, mpld3
# import datetime

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse

# from cart.models import Transaction
from product.models import Product

from .forms import ReviewForm
from .models import Review

# def visualizeMontlyIncome(request):
#     fig = plt.figure(figsize=(4,4))
#     LABELS = ('10', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
#               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',)
#     year = datetime.datetime.now().year
#     transactions = Transaction.objects.filter(timeHis__iso_year=year)
#     data = [0] * 12

#    # print(transactions)
#     for transaction in transactions:
#         data[transaction.timeHis.month-1] += transaction.totalCost
#    # print(data)
#     plt.xlabel(year)
#     plt.ylabel('Income [$]')

#     plt.bar(LABELS, data)
#     # plt.show()
#     http = mpld3.fig_to_html(fig)
#     print(http)
#     return HttpResponse(http)


def homepage_view(request):
    context = {"Products": Product.objects.all}
    return render(request, "product/home.html", context)


def detail_view(request, p_id):
    form = ReviewForm
    context = {"form": form, "Product": Product.objects.get(id=p_id)}

    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                user = request.user
                review = form.cleaned_data.get("review")
                Review(prod_id=p_id, username=user, review=review).save()
                context["reviews"] = Review.objects.filter(prod_id=p_id)
                return render(request, "product/item.html", context)
            else:
                messages.error(request, "You must log in to add a review!")

    context["reviews"] = Review.objects.filter(prod_id=p_id)
    return render(request, "product/item.html", context)
