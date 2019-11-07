# Create your views here.
from django.shortcuts import render

from cart.cart import Cart
from order.forms import OrderForm
from order.models import OrderWithItem
from shop.models import Product


def create_order(request):
    cart = Cart(request)
    # 'if cart.products:' 를 별도로 구성하여 '장바구니가 비었습니다' 안내 페이지로 이동시킬 수 있음
    # 현재 구성은 장바구니가 비어있을 경우, 빈 폼 로드
    if cart.products and request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderWithItem.objects.create(
                    # from order form(model:Order)
                    order=order,
                    # from cart attribute
                    item=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                # 주문 시, 구매 수량만큼 재고 수정
                print(dir(cart.products))
                product = Product.objects.get(id=item['product'].id)
                product.quantity -= item['quantity']
                product.save()
            # 주문 완료 시, 장바구니(session) 비우기
            cart.clear_session()
            return render(request, 'order/created.html', {'order': order})
        else:
            pass
    else:
        form = OrderForm()
        return render(request, 'order/create.html', {'cart': cart, 'form': form})

