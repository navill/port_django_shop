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



## Trouble Shooting - 20191111

- 쿼리셋을 cache에 저장하고, 객체의 속성에 접근 할 때,

  - 객체의 filtering 과정에서 반복적인 데이터베이스 접근

  - ex) view의 products.filter(category=category) 및 template에서 'for product in products' 구문에서 쿼리 발생

    ![image4](/README_Folder/image/trouble1111_1.png)

- Solution

  - cache.get()을 통해 전달받은 쿼리셋을 파이썬 객체로 변환

  - 파이썬 객체의 속성에 접근하기 때문에 데이터베이스에 접근하지 않고도 원하는 동작을 구현할 수 있다.

    ![image5](/README_Folder/image/trouble1111_2.png)

    ```python
        if category_slug:
            for cat in categories:
                if category_slug == cat.slug:
                    category = cat
            products = products.filter(category=category)
            # python 객체로 변환하여, 한 번의 db 접근으로 pagination 및 template에서 사용
            products = [product for product in products]
        paginator = Paginator(products, 6)
        ...
    ```

    

- 고려사항

  - list comprehension을 이용해 파이썬 객체로 변활할 때, 객체가 많은 양의 데이터를 담고 있을 경우, 메모리 낭비가 발생할 수 있다.

  - 따라서 가능하면 제너레이터(lazy evaluation)를 이용해 메모리의 소비를 줄이는 방법을 지양하는 것이 좋다.

    - 위 구문은 paginator의 동작을 위해 필요한 속성(len())을 generator가 가지고 있지 않기 때문에 사용할 수 없다.

    - generator -> list로 변환하여 사용할 수 있지만, 메모리에 대한 이득이 크지 않음.



### Trouble Shooting - 20191113

- 많은 양의 제품 결제 시, 불필요한 db 접근과 많은 시간이 걸림

  - 6개의 아이템 기준 26.95ms이 걸린다.

  - 기존 코드

    ```python
    if cart.products and request.method == 'POST':
        form = OrderForm(request.POST)				
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderWithItem.objects.create(
                  # from order form(model:Order)
                  order=order,
                  # from cart attribute
                  item=item['product'],
                  price=item['price'],
                  quantity=item['quantity']
                )
                # 주문 시, 구매 수량만큼 재고 수정
                product = Product.objects.get(id=item['product'].id)
                product.quantity -= item['quantity']
                product.save()
    ```

    ![trouble1113](/README_Folder/image/trouble1113_1.png)

- solution

  - django 2.2 version에 추가된 [bulk](https://docs.djangoproject.com/en/2.2/ref/models/querysets/#bulk-update)를 이용한 OrderWithItem 생성 및 Product.quantity 업데이트

    ```python
    if products.exists() and request.method == 'POST':
    		form = OrderForm(request.POST)      
    	  if form.is_valid():
            order_item_obj = None
            order_list = []
            order = form.save()
            # dict-type의 Product 객체 생성
            product_bulk = products.in_bulk()
            for item in cart:
                order_item_obj = OrderWithItem(order=order,
                                               item=item['product'],
                                               price=item['price'],
                                               quantity=item['quantity'])
                # OrderWithItem 객체를 리스트에 추가
                order_list.append(order_item_obj)
                product_bulk[item['product'].id].quantity -= item['quantity']
    
                # bulk_create를 이용한 OrderWithItem db 생성
                OrderWithItem.objects.bulk_create(order_list)
                # bulk_update를 이용한 Product.quantity 업데이트
                products.bulk_update(product_bulk.values(), ['quantity'])
    ```

    ![trouble1113](/README_Folder/image/trouble1113_2.png)

    - 6개의 아이템 기준 8.32ms이 걸린다.

    - if 문을 이용해 쿼리 존재 유무를 판단할 때 exists() 메서드를 이용하는 것이 좋음

      - 단, 해당 쿼리문을 이하 블럭에서 사용하지 않을 경우 쿼리문을 쓰는 것이 좋음

        ```python
        # queryset에 접속
        if query_set:
          	# queryset에 한 번 더 접속
          	query_set.get(id=1)
        
        # queryset에 접속하지 않음
        if query_set.exists():
          	# queryset에 접속
        		query_set.get(id=1)
        ```

      