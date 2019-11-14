# Portfolio: django_shop

## App 구성

- Shop - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/shop)
  - 기본적인 쇼핑몰 기능
  - Category와 Product 모델 구성
    - [caching](README_Folder/django_cache.md)을 이용한 제품 출력 페이지 구성 - [shop.views.product_list](https://github.com/navill/port_django_shop/blob/bd3073bce901ea43acee398592e88a5d86120b74/django_shop/shop/views.py#L13)

- Cart - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/cart)
  - [Django Session](README_Folder/django_shop_session.md)을 이용한 장바구니 - [cart.cart.Cart](https://github.com/navill/port_django_shop/blob/de62a57a9f5a27831ca09f74f86c1894b4bb1c19/django_shop/cart/cart.py#L6)
  
- Order - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/order)
  - 장바구니에 담긴 물품을 구매하기 위한 기능
  - 물품 주문 시, [bulk](https://docs.djangoproject.com/en/2.2/ref/models/querysets/#bulk-create)를 이용한 ORM 최적화 - [order.views.create_order](https://github.com/navill/port_django_shop/blob/fd72e1d3dfa46faec563623803a2403eac9d5ae0/django_shop/order/views.py#L15)

- Account - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/account)
  - 사용자 등록 및 유저 정보 변경 기능
    - django.contrib.auth.views를 이용하여 구현
  - 관리자 계정일 경우 유저의 동작 추적(추가예정) - ContentType

### [TroubleShooting](README_Folder/20191106_troubleshooting.md)