## Trouble Shooting

- 짧지만 동일한 쿼리문이 두번 실행됨 
  - cart_detail의 순환문이 실행되면서 product에 대한 쿼리
  - cart_detail 페이지의 템플릿에서 for 문에 의해 product에 대한 쿼리

![problem](/README_Folder/image/problem.png)

- solution

  - Cart.\_iter_ 에 포함된 쿼리문을 Cart.\_init_으로 이동

  - 기존 코드

  ```python
  # cart.Cart
      def __iter__(self):
          product_ids = self.cart.keys()
          self.products = Product.objects.filter(id__in=product_ids)
          for product in self.products:
              self.cart[str(product.id)]['product'] = product
  
  - 수정된 코드
  
  ``` python
  # cart.py
  class Cart:
      def __init__(self, request):
          ...
          product_ids = self.cart.keys()
          self.products = Product.objects.filter(id__in=product_ids)
      
      def __iter__(self):
      		...
    		for product in self.products:
          		self.cart[str(product.id)]['product'] = product
  ```
  
  ![result](/README_Folder/image/result.png)
