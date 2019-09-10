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
    items = []
    totalCost = 0
    if cookie:
        cookie = cookie[:-1].split('/')
        cookie = dict((x, cookie.count(x)) for x in set(cookie))
        p = Product.objects.all()
        for key in cookie:
            try:
                Item = p.get(id=key)
                # print('item', Item)
                items.append([Item.title, cookie[key], str(Item.price)])
                totalCost += cookie[key] * Item.price
            except ObjectDoesNotExist:
                pass

    return items, totalCost


def cart(request):
    cookie = request.COOKIES.get('cartIds')
    items, totalCost = read_cookie(cookie)
    context = {'Items': items, 'totalCost': totalCost}

    if request.method == 'POST':
       # print('CHECK CART')
        discounts = DiscountCode.objects.all()
        code = request.POST.get('discount')
        html = redirect('cart:buyPage')
        for discount in discounts:
            if code == discount.code:
                print('You have a discount')
                cookie = f'{discount.code}/{discount.percent}'
                html.set_cookie('code', cookie, 1800)

        return html

    return render(request, 'cart/cart.html', context)


def addCart(request, cart_id):
    html = redirect('product:homepage')
    # FIX
    i = 1
    cartIds = request.COOKIES.get('cartIds')
    try:
        p = Product.objects.all().get(id=cart_id)
    except ObjectDoesNotExist:
        i = 0
        pass
    if i:
        if request.COOKIES.get('cartIds'):
            cartIds += str(cart_id) + '/'
        else:
            cartIds = ''
            cartIds += str(cart_id) + '/'
        #                'name',     value,  time [s]
        html.set_cookie('cartIds', cartIds, 3600 * 24)
    return html


@login_required
def buyPage(request):
    cartIds = request.COOKIES.get('cartIds')
    code = request.COOKIES.get('code')
    form = UserDataForm
   # print(code)
    items, totalCost = read_cookie(cartIds)
    try:
        code = code.split('/')
        totalCost = Decimal(totalCost-totalCost*int(code[1])/100).quantize(Decimal('.01'))
        context = {'Items': items, 'totalCost': totalCost, 'code': code[0], 'percent': code[1], 'form': form}
    except:
        context = {'Items': items, 'totalCost': totalCost, 'form': form}
        print('error')
    
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            time = datetime.datetime.now()
            print('form valid')
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            print(items)
            trans = Transaction(totalCost=totalCost, items=items, timeHis=time)
            trans.save()
            user.record.add(trans)
            print(user.record.all())

            response = render(request, 'cart/done.html', {})
            response.delete_cookie('cartIds')
            response.delete_cookie('code')
            return response
        else:
            print('form invalid')
    
    return render(request, 'cart/buyPage.html', context)
