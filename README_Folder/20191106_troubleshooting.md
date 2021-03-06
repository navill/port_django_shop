## Query 최적화

- 짧지만 동일한 쿼리문이 두번 실행됨 
  - cart_detail의 순환문이 실행되면서 product에 대한 쿼리
  - cart_detail 페이지의 템플릿에서 for 문에 의해 product에 대한 쿼리

![problem](/README_Folder/image/problem.png)

- **Solution**

  - Cart.\_iter_ 에 포함된 쿼리문을 Cart.\_init_으로 이동

  기존 코드

  ```python
  # cart.Cart
      def __iter__(self):
        product_ids = self.cart.keys()
          self.products = Product.objects.filter(id__in=product_ids)
        for product in self.products:
              self.cart[str(product.id)]['product'] = product
  ```

  수정된 코드


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



## Query 최적화

### 되도록 Cache를 이용한 쿼리 최적화는 지양하는 것이좋다(cache를 유지하기 위한 서버를 동작시키거나 cache 메모리를 유지시키는 것 또한 자원 소모). 

### django에서 제공하는 쿼리 최적화를 위한 메서드나 함수를 이용하고, 오픈소스나 third party library를 이용하자.

- 'home' 페이지 로딩하는데 오랜 시간이 걸림

  - 추천 제품을 화면에 표시할 때, 제품(Product)과 이미지(ProductImage)에 대한 불필요한 쿼리 발생

  ```python
  # models.py
  class Product(models.Model):
      ...
      def get_image_url(self):
          img = self.product_image.first()
          if img:
              # directory path
              return img.image.url
          return img
        
  class ProductImage(models.Model):
      product = models.ForeignKey(Product, related_name='product_image', on_delete=models.CASCADE)
  ```

  

- **Solution(cache - 지양)**
  
  - cache를 이용해 Product 객체를 메모리에 저장
  - 페이지가 리로드될 때, 데이터베이스에 접근하지 않고 메모리에 올라간 Product 객체를 처리

  
  
- **Solution(selete_related)**

  - ProductImage 객체를 가져올 때, select_related를 이용하여 참조에 필요한 Product 객체를 함께 가져온다.

  - product.get_image_url을 이용하는 과정에서 select_related로 가져온 product가 템플릿에서 제대로 사용되지 못 함.

    - get_image_url에서 새로운 참조를 일으키기 때문에 select_related 구문과 별도로 product를 참조하는 쿼리가 발생한다.

      => 1query (ProductImage + Product=JOIN(select_related)에 의해 한 번에 가져옴) + 1query (product.get_image_url=Product 객체가 한번 더 ProductImage를 호출)
  - 때문에 models.py와 함께 template도 추가로 변경

  ```python
    {% for product_image in product_images %}
      {% with product_image.product as product %}
      ...
    {% endwith %}
    {% endfor %}
  ```

    - with tag를 이용해 기존의 product 변수명은 유지하고 product_image는 기존의 get_image_url을 대체 한다.

  

    

- **고려사항**

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




## Query 최적화

- 쿼리셋을 cache에 저장하고, 객체의 속성에 접근 할 때,

  - 객체의 filtering 과정에서 반복적인 데이터베이스 접근

  - ex) view의 products.filter(category=category) + template에서 'for product in products' 구문에서 쿼리 발생

    ![image4](/README_Folder/image/trouble1111_1.png)

- **Solution**

  - cache.get()을 통해 전달받은 캐싱된 쿼리셋을 이용

  - 메모리에 저장된 데이터에 접근하기 때문에 데이터베이스에 접근하지 않고도 원하는 동작을 구현할 수 있다.

    ![image5](/README_Folder/image/trouble1111_2.png)

    ```python
        if category_slug:
            for cat in categories:
                if category_slug == cat.slug:
                    category = cat
            products = products.filter(category=category)
            # 한 번의 db 접근으로 pagination 및 template에서 사용
            products = [product for product in products]
        paginator = Paginator(products, 6)
        ...
    ```

    

- 고려사항

  - list comprehension을 이용할 때, 객체가 많은 양의 데이터를 담고 있을 경우, 메모리 낭비가 발생할 수 있다.

  - 따라서 가능하면 제너레이터(lazy evaluation)를 이용해 메모리의 소비를 줄이는 방법을 지향하는 것이 좋다.

    - 위 구문은 paginator의 동작을 위해 필요한 속성(len())을 generator가 가지고 있지 않기 때문에 사용할 수 없다.



### Bulk를 이용한 쿼리문 처리 

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

- **Solution**

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

      ```python
      # query에 접속
      if query_set:
          # query에 한 번 더 접속
          query_set.get(id=1)
      
      # query에 접속하지 않음
      if query_set.exists():
          # query에 접속
          query_set.get(id=1)
      ```

      

### itertools.combinations을 이용한 조합 생성 

- 이중 for문을 이용한 구조를 변경하고자 함

```python
    # before
    def buy_item(self, products):
        if self.connect_status:
            product_ids = [p.id for p in products]
            for product_id in product_ids:
                r.zincrby('product', value=product_id, amount=1)
                for with_id in product_ids:
                    # product_id + product_id를 피하기 위한 조건문
                    # -> A, B, C를 함께 구매할 경우 (A,B), (A,C), (B,C)만 해당, A,A는 제외되어야 한다.
                    if product_id != with_id:
                        r.zincrby(f'product:{product_id}', value=with_id, amount=1)
    # after
    def buy_item(self, products):
        if self.connect_status:
            product_ids = [p.id for p in products]
            com_ids = itertools.combinations(product_ids, len(product_ids) - 1)
            for ids in com_ids:
                product_id = list(set(product_ids) - set(ids))
                product_id = int(product_id[0])
                partial_zincrby = partial(r.zincrby, name=f'product:{product_id}', amount=1)
                list(map(lambda value: partial_zincrby(value=value), ids))
```

- **Solution**
  - itertools.combination을 이용한 조합을 생성하고 한 번의 순환문(코드 상에서)을 이용해 zincrby 실행



- **Result**

  ```python
# testcode
  
@benchmarker_time
  @profile(precision=4)
def func_a(product_ids):
      for item in product_ids:
        for item2 in product_ids:
              if item != item2:
                print(item2)
  
@benchmarker_time
  @profile(precision=4)
def func_b(product_ids):
      # 조합 생성
    li = itertools.combinations(product_ids, len(product_ids) - 1)
      for item2 in li:
          item = set(product_ids) - set(item2)
          for i in item2:
              print(i)
  ```
  
  - before: 메모리 측면에서 더 좋은 성능을 보이지만 속도가 느림
  
  ![20191210_before](/README_Folder/image/20191210_before.png)
  
  - after: 메모리 측면에서 효율이 떨어지지만, 속도의 차이가 있음
  
  ![20191210_after](/README_Folder/image/20191210_after.png)
  
  - 빠른 속도를 제공해야하는 서비스에서는 itertools를 이용하는 것이 더 좋은 성능을 보일 수 있다.
  
  - 하지만 객체의 수(제품)가 많지 않을 경우 큰 이득을 취할 수 없다.
  
  - 메모리 효율에 대해서는 좀 더 조사가 필요하다.
  
    - for문을 이용할 때 메모리 증가치가 0인 이유를 확인하지 못함
  
      -> 실제로 메모리 증가가 이루어지지 않는지, 테스트상 오류인지 확인되지 않음



### Singleton을 이용한 불필요한 객체 생성 제한 

- 일부 객체가 불필요하게 새로 생성된다.

- 메모리에 불필요한 새로운 객체가 지속적으로 할당될 경우 서비스가 적절한 성능을 낼 수 없다.

  **Cart 객체 생성 시** 

  - add, detail, clear, context_processor 동작 시 모두 새로운 Cart 객체가 생성됨

  ![20191212_before_singleton](/README_Folder/image/20191212_before_singleton.png)

  **Recommender 객체 생성 시**

  - 각 페이지를 이동할 때 마다 Recommender의 객체가 새로 생성됨

  ![20191212_before_single_reco](/README_Folder/image/20191212_before_single_reco.png)

- **Solution**

  - Cart는 session에서, Recommend는 Redis에서 데이터를 불러와서 처리하기 때문에 동작마다 새로운 객체를 생성할 필요가 없다.

  - singleton pattern을 이용하여 하나의 identity를 갖는 객체를 생성하여 불필요한 메모리 낭비를 줄일 수 있다.

    ```python
    class Singleton:
        _instance = None
    
        def __new__(cls, *args):
            # Cart의 객체인지 확인
            # 아래 조건문이 True 경우, 새로운 cls._instance 생성 후 반환, False일 경우 None 반환
            if not isinstance(cls._instance, cls):
                cls._instance = object.__new__(cls)
            return cls._instance
    ```

    - singleton을 구현하는 방법은 여러가지이며 각각 장단점을 갖기 때문에 목적에 따라 구현법을 달리 할 수 있다.

- **Result**

  **Cart 객체 생성**

  ![20191212_after_singleton](/README_Folder/image/20191212_after_singleton.png)

  **Recommend 객체 생성**

  ![20191212_after_single_reco](/README_Folder/image/20191212_after_single_reco.png)

  - 각각 다른 동작을 위해 객체가 생성되더라도 동일한 id값을 갖는다. 
  - Singleton 패턴이 적용된 객체는 다른 앱에서 객체를 생성하여 db나 공유 객체에 접근할 수 없기 때문에 race condition을 해결하기 위한 방법으로도 쓰인다.
  
  
  
- **Additional**

  - 몇가지 singleton에 관한 테스트

    ```python
    # 1: TypeError: getinstance() takes 1 positional argument but 4 were given
    # 두 번째 객체 생성 시 에러 발생
    class SingletonInstance:
        __instance = None
    
        @classmethod
        def getinstance(cls):
            return cls.__instance
    
        @classmethod
        def instance(cls, *args, **kwargs):
            cls.__instance = cls(*args, **kwargs)
            cls.instance = cls.getinstance
            return cls.__instance
    
    
    class MainClass(SingletonInstance):
        def __init__(self, a, b, c):
            self.result = a + b + c
    
    ---------------------------------------------------------
    # 2: 새로운 객체 생성 -> init을 포함한 객체가 _instances에 할당
    # -> 새로운 객체에 의해 생성된 초기화값은 무시됨
    class SingletonType(type):
        # _instances: 초기화된 MainClass가 들어가기 때문에 동일한 클래스로
        # 객체 생성 시, 새로운 값으로 초기화되지 않는다.
        _instances = {}
    
        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
    
    
    class MainClass(metaclass=SingletonType):
        # 새로운 객체를 생성하더라도 정체성이 변하지 않지만,
        # 초기화된 값 또한 변하지 않기 떄문에 주의
        # 함수를 실행하기 위한 목적으로 사용
        def __init__(self, a, b, c):
            self.result = a + b + c
    
    
    a = MainClass(1, 2, 3)
    print(a.result)  # 6
    print(id(a))  # 4565035048
    b = MainClass(3, 4, 5)
    print(b.result)  # 6
    print(id(b))  # 4565035048
    
    ---------------------------------------------------------
    # 3: 새로운 객체 생성 시, 정체성(id)는 바뀌지 않지만 초기화(__init__)은 반영
    class Singleton:
        _instance = None
    
        def __new__(cls, *args):
            if not isinstance(cls._instance, cls):
                # 객체 생성 후 아래의 MainClass에서 초기화가 이루어지기 때문에
                # 새로운 객체의 초기화값은 반영된다.
                cls._instance = object.__new__(cls)
            return cls._instance
    
    
    class MainClass(Singleton):
        def __init__(self, a, b, c):
            self.result = a + b + c
    
    
    a = MainClass(1, 2, 3)
    print(a.result)  # 6
    print(id(a))  # 4565035664
    b = MainClass(3, 4, 5)
    print(b.result)  # 12
    print(id(b))  # 4565035664
    
    ---------------------------------------------------------
    # 4(from sourcemaking): 2번과 동일한 결과
    class Singleton(type):
        """
        Define an Instance operation that lets clients access its unique
        instance.
        """
    
        def __init__(cls, name, bases, attrs, **kwargs):
            print(name, bases, attrs)
            super().__init__(name, bases, attrs)
            cls._instance = None
    
        def __call__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super().__call__(*args, **kwargs)
            return cls._instance
    
    
    class MainClass(metaclass=Singleton):
        def __init__(self, a, b, c):
            self.result = a + b + c
    
    
    a = MainClass(1, 2, 3)
    print(a.result)  # 6
    print(id(a))  # 4545081528
    b = MainClass(3, 4, 5)
    print(b.result)  # 6
    print(id(b))  # 4545081528
    ---------------------------------------------------------
    
    ```
    
  - 객체를 새로 생성할 때 마다 객체 자체의 정체성(identity)은 변하지 않고, 입력된 값은 반영 되어야 할 경우, 3번을 제외한 나머지는 사용 불가