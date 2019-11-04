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
    product = get_object_or_404(Product, id=product_id)
    form = CartForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'])
    else:
        pass
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['cart_form'] = CartForm(initial={'quantity': item['quantity']})

    return render(request, 'cart/detail.html', {'cart': cart})
