# Portfolio: django_shop

## App 구성

- Shop - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/shop)
  - 기본적인 쇼핑몰 기능
  - Category와 Product 모델 구성
    - [caching](README_Folder/django_cache.md)을 이용한 제품 출력 페이지 구성 - views.product_list
- Cart - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/cart)
  - [Django Session](README_Folder/django_shop_session.md)을 이용한 장바구니
  - cart.py - Cart class
- Order - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/order)
  - 장바구니에 담긴 물품을 구매하기 위한 기능


### [TroubleShooting](README_Folder/20191106_troubleshooting.md)
