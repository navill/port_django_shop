- ## Trouble Shooting - 20191106

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
    ```
    
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
  
  
  
  ## Trouble Shooting - 20191107
  
  ![image1](/README_Folder/image/trouble1107_1.png)
  
  - product_list 페이지 로딩하는데 오랜 시간이 걸림
  
    - 모든 product_list에서 Product.objects.all() 및 Category.objects.all()이 일어남 
      - 비교적 많은 양의 데이터를 가지고 있음
    - pagination 과정에서 db에 많은 접근(예상)
  
    
  
  - Solution
  
    - cache를 이용해 Product 객체를 메모리에 저장
    - 페이지가 로드될 때, 데이터베이스에 접근하지 않고 메모리에 올라간 Product 객체를 처리
  
    ![image2](/README_Folder/image/trouble1107_2.png)
  
  
  
  - 고려사항
  
    ```python
        if category_slug:
            category = categories.get(slug=category_slug)
            products = products.filter(category=category)
    ```
  
    - 코드를 위와 같이 구성할 경우 categories.get() 메서드에 의해 데이터베이스에 접근하게 됨
    - 따라서 쿼리 객체를 처리할 경우 db에 접근할 수 있는 메서드의 사용을 지양해야함
  
    ```python
        for cat in categories:
          	if category_slug == cat.slug:
            		category = cat
            products = products.filter(category=category)
    ```
  
    - 아래의 그림은 categories.get()을 사용할 경우
  
    ![image3](/README_Folder/image/trouble1107_3.png)