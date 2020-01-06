# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartForm
from shop.models import Product


@require_POST
def cart_add(request, product_id):
    # 요청자의 session을 이용해 Cart 객체 생성
    cart = Cart(request)
    # print('id(cart) in cart_add:', id(cart))
    product = get_object_or_404(Product, id=product_id)
    # CartForm includes quantity and is_update
    # quantity: item quantity
    # is_update: determine whether it will be updated
    #     -> it is only 'True' when cart_detail works
    form = CartForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])
        print(cd['is_update'])
    else:
        cart.add(product=product, quantity=1, is_update=False)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    # print('id(cart) in cart_remove:', id(cart))
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    # print('id(cart) in cart_detail:', id(cart))
    for item in cart:
        # quantity 및 is_update 데이터를 담고 있는 폼을 cart-session에 저장
        # item = {'1':{'quantity': 1, 'price': 10, cartform:<..., fields = (quantity, is_update)>}}
        item['cart_form'] = CartForm(initial={'quantity': item['quantity'], 'is_update': True})
        # print(item['cart_form'])
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_clear(request):
    cart = Cart(request)

    # print('id(cart) in cart_clear:', id(cart))
    cart.clear_cart()
    return redirect(request.META['HTTP_REFERER'])
