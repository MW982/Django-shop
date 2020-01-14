import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponseRedirect

from product.models import Product
from cart.models import Transaction, DiscountCode
from main.models import User
from main.forms import UserDataForm

from decimal import Decimal


def read_cookie(cookie):
    items, total_cost = [], 0
    if not cookie:
        return items, total_cost

    cookie = cookie[:-1].split("/")
    cookie = dict((int(x), cookie.count(x)) for x in set(cookie))
    products = Product.objects.filter(pk__in=cookie.keys())
    for product in products:
        items.append([product.title, cookie[product.pk], str(product.price)])
        total_cost += cookie[product.pk] * product.price

    return items, total_cost


def cart_view(request):
    cookie = request.COOKIES.get("cartIds")
    items, total_cost = read_cookie(cookie)
    context = {"Items": items, "totalCost": total_cost}

    if request.method == "POST":
        discounts = DiscountCode.objects.all()
        code = request.POST.get("discount")
        html = redirect("cart:buyPage")
        for discount in discounts:
            if code == discount.code:
                cookie = f"{discount.code}/{discount.percent}"
                html.set_cookie("code", cookie, 1800)

        return html

    return render(request, "cart/cart.html", context)


def add_cart_view(request, cart_id):
    html = redirect("product:homepage")
    i = 1
    cart_ids = request.COOKIES.get("cartIds")
    try:
        products = Product.objects.all().get(id=cart_id)
    except ObjectDoesNotExist:
        i = 0
        pass
    if i:
        if request.COOKIES.get("cartIds"):
            cart_ids += str(cart_id) + "/"
        else:
            cart_ids = ""
            cart_ids += str(cart_id) + "/"
        #                'name',     value,  time [s]
        html.set_cookie("cartIds", cart_ids, 3600 * 24)
    return html


@login_required
def buy_page_view(request):
    cart_ids = request.COOKIES.get("cartIds")
    code = request.COOKIES.get("code")
    form = UserDataForm
    items, total_cost = read_cookie(cart_ids)
    try:
        code = code.split("/")
        total_cost = Decimal(totalCost - totalCost * int(code[1]) / 100).quantize(
            Decimal(".01")
        )
        context = {
            "Items": items,
            "totalCost": total_cost,
            "code": code[0],
            "percent": code[1],
            "form": form,
        }
    except:
        context = {"Items": items, "totalCost": total_cost, "form": form}

    if request.method == "POST":
        form = UserDataForm(request.POST)
        if form.is_valid():
            time = datetime.datetime.now()
            email = form.cleaned_data.get("email")
            user = User.objects.get(email=email)
            trans = Transaction(totalCost=total_cost, items=items, timeHis=time)
            trans.save()
            user.record.add(trans)

            response = render(request, "cart/done.html", {})
            response.delete_cookie("cartIds")
            response.delete_cookie("code")
            return response

    return render(request, "cart/buyPage.html", context)
