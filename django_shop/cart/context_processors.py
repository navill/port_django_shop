from cart.cart import Cart


def cart(request):
    cart = Cart(request)
    # print('cart(id) in context:', id(cart))
    return {'cart': cart}
