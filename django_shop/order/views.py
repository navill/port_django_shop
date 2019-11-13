# Create your views here.
from django.shortcuts import render

from account.actions import track_action
from cart.cart import Cart
from order.forms import OrderForm
from order.models import OrderWithItem


def create_order(request):
    cart = Cart(request)
    # 'if cart.products:' 를 별도로 구성하여 '장바구니가 비었습니다' 안내 페이지로 이동시킬 수 있음
    # 현재 구성은 장바구니가 비어있을 경우, 빈 폼 로드
    products = cart.products
    if products.exists() and request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_item_obj = None
            order_item_list = []
            order = form.save()
            # dict-type의 Product 객체 생성
            product_bulk = products.in_bulk()
            for item in cart:
                order_item_obj = OrderWithItem(order=order,
                                           item=item['product'],
                                           price=item['price'],
                                           quantity=item['quantity'])
                # OrderWithItem 객체를 리스트에 추가
                order_item_list.append(order_item_obj)
                product_bulk[item['product'].id].quantity -= item['quantity']

            # bulk_create를 이용한 OrderWithItem db 생성
            OrderWithItem.objects.bulk_create(order_item_list)
            # bulk_update를 이용한 Product.quantity 업데이트
            products.bulk_update(product_bulk.values(), ['quantity'])
            # 주문 완료 시, 장바구니(session) 비우기
            cart.clear_session()
            # 사용자 동작
            if request.user.is_authenticated:
                # user=Foreignkey(User) 이므로 request.user가 authenticated user가 아닐 경우 에러 발생
                track_action(user=request.user, verb='buy', content_object=order_item_obj)
            return render(request, 'order/created.html', {'order': order})
        else:
            pass
    else:
        form = OrderForm()
        return render(request, 'order/create.html', {'cart': cart, 'form': form})
