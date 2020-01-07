# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render

from account.actions import track_action
from cart.cart import Cart
from order.forms import OrderForm
from order.models import OrderWithItem, Order
from shop.recommender import Recommend

User = get_user_model()


def user_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderWithItem.objects.filter(order=order)
    if request.user == order.user:
        return render(request, 'order/created.html', {'order': order, 'order_items': order_items})


def create_order(request):
    cart = Cart(request)
    # 'if cart.products:' 를 별도로 구성하여 '장바구니가 비었습니다' 안내 페이지로 이동시킬 수 있음
    # 현재 구성은 장바구니가 비어있을 경우, 빈 폼 로드
    products = cart.products  # cart에 담긴 아이템들
    total_price = cart.get_total_price()  # 총 가격
    if products.exists() and request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_item_list = []
            order = form.save(commit=False)
            order.total_price = total_price
            order.user = request.user
            order.save()
            # dict-type의 Product 객체 생성
            product_bulk = products.in_bulk()
            for item in cart:
                order_item_obj = OrderWithItem(order=order,
                                               item=item['product'],
                                               price=int(item['price']) * int(item['quantity']),
                                               quantity=item['quantity'])
                # OrderWithItem 객체를 리스트에 추가
                order_item_list.append(order_item_obj)
                product_bulk[item['product'].id].quantity -= item['quantity']
                # 사용자 동작
                if request.user.is_authenticated:
                    # user=Foreignkey(User) 이므로 request.user가 authenticated user가 아닐 경우 에러 발생
                    track_action(user=request.user, verb='bought', content_object=item['product'])

            # bulk_create를 이용한 OrderWithItem db 생성
            order_items = OrderWithItem.objects.bulk_create(order_item_list)
            # bulk_update를 이용한 Product.quantity 업데이트(release version2.2)
            products.bulk_update(product_bulk.values(), ['quantity'])
            # 함께 구매한 아이템 등록
            r = Recommend()
            try:
                r.buy_item(products)
            except Exception as e:
                print(f'not connect redis:{e}')

            # for order_item in order_items:
            #     print(order_item.order.id)  # 주문번호
            #     print(order_item.item)      # 아이템
            #     print(order_item.price)     # 가격
            #     print(order_item.quantity)  # 수량

            # 주문 완료 시, 장바구니(session) 비우기
            cart.clear_session()
            return render(request, 'order/created.html', {'order': order, 'order_items': order_items})
            # order -> 주문번호, 사용자 성, 이름, 주소, 구매 총 가격
            # order_item -> 구매 아이템 수량, 가격

    else:
        user = User.objects.get(id=request.user.id)

        form = OrderForm(
            initial={'first_name': user.first_name, 'last_name': user.last_name, 'address': user.profile.address,
                     'post_code': user.profile.postal_code})
        print(form['address'])
        return render(request, 'order/create.html', {'cart': cart, 'form': form})
