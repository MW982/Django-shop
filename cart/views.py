from django.shortcuts import render, redirect

from product.models import Product

from main.forms import UserDataForm



def cart(request):
    Items = request.COOKIES.get('cartIds')
    totalCost = 0
    print(Items)
    Fitems = []
    if request.method == 'POST':
        print('CHECK CART')
        return redirect('cart:buyPage')
    
    if Items:
        Items = Items[:-1].split('/')
        Items = dict((x,Items.count(x)) for x in set(Items))
        p = Product.objects.all()
        totalCost = 0
        for key in Items:
            try:
                Item = p.get(id=key)
                print('item', Item)
                Fitems.append([Item.title, Items[key], Item.price])
                totalCost += Items[key] * Item.price
            except:
                pass            

    print('Fi', Fitems)

    return render(request, 'main/cart.html', {'Items': Fitems, 'totalCost': totalCost})


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
            print('form valid')
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email)
        else:
            print('form invalid')

    
    form = UserDataForm
    return render(request, 'main/buyPage.html', {'form': form})

