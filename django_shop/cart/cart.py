from django.conf import settings

# cart = {product_id:{quantity:0, price:0}, product_id:{}...}
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            self.session[settings.CART_SESSION_ID] = {}
            cart = self.session[settings.CART_SESSION_ID]
        self.cart = cart

    # 장바구니 담기 - session 추가
    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            # int(product.id)일 경우 -> session.get()에서 검색할 수 없음
            # -> 처음에는 product_id를 숫자로 세션에 저장, session.get()을 이용해 받을 때 key 값이 문자열로 변경되어 넘어옴
            # -> 때문에 이후 키 값을 지정할 때, id를 문자열로 변경한 후 처리해야 한다.
            self.cart[product_id] = {'quantity': 0, 'price': product.price}
        # todo: 카트의 수량을 변경하지 않은 상태에서 update를 누를 경우 수량이 누적되는 문제
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
        # self.cart = {'1':{'quantity': 1, 'price': 10}} -> product.id를 문자열로 변환
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # 장바구니 수정
    def update(self):
        pass

    # 장바구니에 담긴 품목 총 가격
    def get_total_price(self):
        total_price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return total_price

    # cart에 대한 iterable 속성 부여
    # detail 페이지에서 cart 객체에 대한 iterator가 필요
    # + cart_detail page에서 필요한 데이터 추
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # 카트에 포함된 제품들의 모든 수량
        return sum(item['quantity'] for item in self.cart.values())
