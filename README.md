# port_django_shop

## App 구성

- [Shop](https://github.com/navill/port_django_shop/tree/master/django_shop/shop) - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/shop)
  - 기본적인 쇼핑몰 기능
  - Category와 Product 모델 구성
- [Cart](https://github.com/navill/port_django_shop/tree/master/django_shop/cart) - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/cart)
  - Django Session을 이용한 장바구니
  - cart.py - Cart class
    - \__init__: 요청자로부터(request.session) 전달받은 세션을 cart 객체에 저장
    - \__iter__: cart 객체에 iteratable 속성을 부여하기 위한 overriding
- Order
  - 장바구니에 담긴 물품을 구매하기 위한 기능

