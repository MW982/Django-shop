import datetime

from django.shortcuts import render, redirect, HttpResponseRedirect

from product.models import Product
from cart.models import TransactionHistory
from main.models import User
from main.forms import UserDataForm

def read_cart_cookie(cookie):
    items = []
    totalCost = 0 
    if cookie:
        cookie = cookie[:-1].split('/')
        cookie = dict((x,cookie.count(x)) for x in set(cookie))
        p = Product.objects.all()
        for key in cookie:
            try:
                Item = p.get(id=key)
                #print('item', Item)
                items.append([Item.title, cookie[key], str(Item.price)])
                totalCost += cookie[key] * Item.price
            except:
                pass

    return items, totalCost

def cart(request):
    cookie = request.COOKIES.get('cartIds')
    print(cookie)
    if request.method == 'POST':
        print('CHECK CART')
        return redirect('cart:buyPage')
    
    items, totalCost = read_cart_cookie(cookie)
    return render(request, 'cart/cart.html', {'Items': items, 'totalCost': totalCost})

def addCart(request, cart_id):
    html = redirect('product:homepage')
    #html = render(request, 'main/home.html', context={})
    #html = HttpResponse()
    #FIX
    i = 1
    cartIds = request.COOKIES.get('cartIds')
    try:
        p = Product.objects.all().get(id=cart_id)
    except:
        i = 0
        pass
    if i:
        if request.COOKIES.get('cartIds'):
            cartIds += str(cart_id) + '/'
        else:
            cartIds = ''
            cartIds += str(cart_id) + '/'
        #               'name',     value,  time [s] 
        html.set_cookie('cartIds', cartIds, 3600 * 24 )
    return html 

def buyPage(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            time = datetime.datetime.now()
        #    print('form valid')
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)

            cookie = request.COOKIES.get('cartIds')
            items, totalCost = read_cart_cookie(cookie)
            transHistory = TransactionHistory(totalCost=totalCost, items=items, timeHis=time)
            transHistory.save()
            user.buyRecord.add(transHistory)
            print(user.buyRecord.all())

            respone = render(request, 'cart/done.html', {})
            respone.delete_cookie('cartIds')
            return respone
        else:
            print('form invalid')

    form = UserDataForm
    return render(request, 'cart/buyPage.html', {'form': form})

