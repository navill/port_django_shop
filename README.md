# Portfolio: django_shop

**django shop**: http://django.navill.shop/

**PPT**: [Google Drive(PDF)](https://drive.google.com/file/d/1pseR-K55QMxrJqaDQHK2MGOJDZAhoV7g/view?usp=sharing)

## App 구성

- Shop - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/shop)
  - 기본적인 쇼핑몰 기능
  - Category와 Product 모델 구성
    - [caching](README_Folder/django_cache.md)(memcached)을 이용한 제품 출력 페이지 구성 - [shop.views.product_list](https://github.com/navill/port_django_shop/blob/bd3073bce901ea43acee398592e88a5d86120b74/django_shop/shop/views.py#L13)
  - [Redis](README_Folder/redis.md)를 이용한 best seller 및 함께 구매한 제품 추천 기능 - [shop.recommender.Recommend](https://github.com/navill/port_django_shop/blob/fbee725b131d1584e0578d92006bf182d07d4f1f/django_shop/shop/recommender.py#L14)
  - Singleton을 이용한 Cart 및 Recommend 객체 생성 - [shop.pattern_singletone](https://github.com/navill/port_django_shop/blob/master/django_shop/shop/pattern_singleton.py)
  
- Cart - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/cart)
  - [Django Session](README_Folder/django_shop_session.md)을 이용한 장바구니 - [cart.cart.Cart](https://github.com/navill/port_django_shop/blob/de62a57a9f5a27831ca09f74f86c1894b4bb1c19/django_shop/cart/cart.py#L6)
  
- Order - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/order)
  - 장바구니에 담긴 물품 구매 단계
  - 물품 주문 시, [bulk](https://docs.djangoproject.com/en/2.2/ref/models/querysets/#bulk-create)를 이용한 ORM 최적화 - [order.views.create_order](https://github.com/navill/port_django_shop/blob/fd72e1d3dfa46faec563623803a2403eac9d5ae0/django_shop/order/views.py#L15)

- Account - [git](https://github.com/navill/port_django_shop/tree/master/django_shop/account)
  - 사용자 등록 및 유저 정보 변경 기능
    - django.contrib.auth.views를 이용하여 구현
  - ~~관리자 계정일 경우 유저의 동작 추적~~([ContentType](README_Folder/contenttype.md))

### [TroubleShooting](README_Folder/20191106_troubleshooting.md)

- [QuerySet](https://github.com/navill/port_django_shop/blob/master/README_Folder/20191106_troubleshooting.md#queryset-최적화---1): 반복적인 데이터 베이스 접근을 해결하고 서비스의 성능을 높이기 위한 QuerySet 최적화

- [Bulk를 이용한 쿼리문 처리](https://github.com/navill/port_django_shop/blob/master/README_Folder/20191106_troubleshooting.md#bulk를-이용한-쿼리문-처리): 여러 객체를 한꺼번에 생성하거나 업데이트 해야할 경우 반복문이 아닌 bulk 함수를 이용하여 빠른 성능을 구현
- [itertools.combinations](https://github.com/navill/port_django_shop/blob/master/README_Folder/20191106_troubleshooting.md#itertoolscombinations을-이용한-조합-생성)을 이용한 조합 생성: 이중 for 문을 이용한 요소 조합이 아닌 최적화된 built-in 함수를 이용하여 중복되지 않는 요소 조합 생성
- [Singleton을 이용한 불필요한 객체 생성 제한](https://github.com/navill/port_django_shop/blob/master/README_Folder/20191106_troubleshooting.md#singleton을-이용한-불필요한-객체-생성-제한): Singleton 패턴을 이용해 불필요한 객체 생성을 줄임으로써 성능 저하 요소 제거

