from django.conf import settings

from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        # session.get(): 세션에 구성된 데이터의 키값이 숫자일 경우 문자열로 변환되어 전달된다.
        # -> 데이터에 접근할 때 숫자로 된 키값을 문자열로 변환해서 사용해야 함
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            self.session[settings.CART_SESSION_ID] = {}
            cart = self.session[settings.CART_SESSION_ID]
        self.cart = cart
        # cart_detail 및 templates에서 동일한 쿼리가 발생하는 문제
        # -> query 문의 위치를 __iter__가 아닌 __init__에 정의
        product_ids = self.cart.keys()
        self.products = Product.objects.filter(id__in=product_ids)

    # 장바구니 담기 - session 추가
    def add(self, product, quantity=1, is_update=False):
        # int(product.id)일 경우 -> self.cart[product_id] 값을 검색할 수 없음
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': product.price}
        if is_update:
            # is_update=True(update) 일 때 -> cart = quantity
            self.cart[product_id]['quantity'] = quantity
        else:
            # is_update=False(add) 일 때 -> cart += quantity
            self.cart[product_id]['quantity'] += quantity
        self.save()

    # session 저장
    def save(self):
        # request 발생 시, session.modified를 확인하고 session을 저장할지 여부를 판단
        self.session.modified = True

    # 장바구니 비우기 - session 삭제
    def clear_session(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    # 해당 아이템 비우기 - session 수정
    def remove_product(self, product):
        # ex) self.cart = {'1':{'quantity': 1, 'price': 10}} -> product.id를 문자열로 변환
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # 장바구니에 담긴 품목 총 가격
    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    # cart에 대한 iterable 속성 부여
    # detail 페이지에서 cart 객체에 대한 iterator가 필요
    def __iter__(self):
        for product in self.products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            # unit price
            item['total_price'] = item['price'] * item['quantity']
            # generator -> iterator로서 동작
            yield item

    def __len__(self):
        # 카트에 포함된 제품들의 모든 수량
        return sum(item['quantity'] for item in self.cart.values())
