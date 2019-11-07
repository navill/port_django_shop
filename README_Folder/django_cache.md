### Django Cache

[Django's cache framework | Django documentation | Django](https://docs.djangoproject.com/en/2.2/topics/cache/)

- Django에서 제공하는 cache backend - Memory 기반 cache가 높은 성능을 발휘

  - `backends.memcached.MemcachedCache` or `backends.memcached.PyLibMCCache`:  메모리 기반 cache
  - `backends.db.DatabaseCache`: db를 이용한 cache
  - `backends.filebased.FileBasedCache`: 파일을 이용한 cache
  - `backends.locmem.LocMemCache`: 로컬 메모리 기반 cache
  - `backends.dummy.DummyCache`: 개발 환경 cache

- install memcached

  ```
    $ brew install memcached
    $ pip install python-memcached
  ```

- setting cache

  ```
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
  ```

- memcached initialize

  ```
    memcached -l 127.0.0.1:11211
  ```

- Cache setting

  - ```
    CACHES
    ```

    : dictionary 형태로 프로젝트에서 사용 가능한 모든 캐쉬 설정 

    - `BACKEND`: 사용할 캐쉬
    - `KEY_FUNCTION`: 접두사, 버전 및 키를 인수로 사용하고 최종 캐시 키를 반환하는 콜 러블에 대한 점선 경로가 포함 된 문자열
    - `KEY_PREFIX`: 충돌을 피하기 위해 모든 캐시 키의 문자열 접두사
    - `LOCATION`: 캐시의 위치. 캐시 백엔드에 따라 디렉토리, 호스트 및 포트 또는 인 메모리 백엔드의 이름 일 수 있습니다
    - `OPTIONS`: 캐시 백엔드로 전달 될 추가 매개 변수
    - `TIMEOUT`: 캐시 키를 저장하기 위한 기본 제한 시간 (초, default: 300s). None으로 설정하면 캐시 키가 만료되지 않음
    - `VERSION`: 캐시 키의 기본 버전 번호(버전 관리를 위해 사용)

  - `CACHE_MIDDLEWARE_ALIAS`: 저장 공간에 사용할 캐쉬의 별칭

  - `CACHE_MIDDLEWARE_KEY_PREFIX`: 캐시 키에 사용할 접두사

  - `CACHE_MIDDLEWARE_SECONDS`: 캐시 페이지를 로드하기 위한 기본적인 시간(초)

- memcache monitoring

  ```python
    $ pip install django-memcache-status
  
    # admin.py
    from django.contrib import admin
    admin.site.index_template = 'memcache_status/admin_index.html'
    
    # settings.py
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
  ```

  ![cache_status](/Users/jh/Desktop/스크린샷 2019-11-01 오후 8.50.29.png)

  - curr item: cache에 저장된 아이템 개수

  - get hits: cache.get이 성공한 횟수

  - get misses: cache.get이 실패한 횟수

    

- Django에서 제공하는 캐쉬 레벨

  - **Low-level cache API**: 쿼리 및 각종 연산에 대한 캐쉬(가장 낮은 수준의 캐쉬)
  - **Per-view cache**: 뷰에 대한 캐쉬
  - **Template cache**: 템플릿에 대한 캐쉬
  - **Per-site cache**: 해당 사이트에 대한 캐쉬(가장 높은 수준의 캐쉬)

- python shell을 이용한 기본 동작

  - syntax

    - set(key, value, timeout)

    - get(key)

    - ```python
      from django.core.cache import cache 
      cache.set('django', 'python', 20) 
      cache.get('django') 
      'python' 
      # (20초 후)
      cache.get('django')
      # 출력 없음
      
      from courses.models import Subject 
      subjects = Subject.objects.all() 
      cache.set('all_subjects', subjects) 
      cache.get('all_subjects') 
      <QuerySet [<Subject: Mathmetics>, <Subject: Music>, <Subject: Physics>, <Subject: Programming>]>
      ```

    

  - cache miss와 None을 구분하지 못하기 때문에, value에 None을 입력하지 말아야 한다.

  - view 실행 시, cache를 이용해 로드 → cache없을 경우 db로부터 객체를 불러오고 cache.set()

    ```python
      def get(self, request):
          items = cache.get('all_item')
          if not items:
              items = Product.objects.all()
              cache.set('all_item', items)
    
    ```

  

  

  