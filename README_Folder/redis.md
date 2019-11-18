# Redis(Remote dictionary server)

- ‘키-값’ 구조의 비관계형 데이터를 저장하고 관리하기 위한 NoSQL의 일종
- 문자열, 해시, 목록, 세트, 정렬된 세트 비트맵 등 다양한 데이터 구조를 지원
- 캐시 또는 빠른 속도로 데이터가 변화(수정)할 때 높은 성능을 발휘

------

### redis - make 명령어 오류(Mac OS)

```python
# problem
xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun

# solution
$ xcode-select --install
```

------

### Redis 설치

- https://redis.io/download에서 압축 파일 다운 + 해제

  ```python
    # redis 디렉토리 이동
    cd redis-4.0.9
    # install redis
    make  
    # redis server 실행
    src/redis-server
    # redis client 실행
    $ src/redis-cli 127.0.0.1:6379>
  ```

  - default port: 6379

  - python shell을 이용한 테스트

    ```python
    >>> import redis
    >>> r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    >>> r.set('foo', 'bar')
    True
    >>> r.get('foo')
    b'bar'
    ```

  - Redis는 StrictRedis의 하위 클래스로서 이전 버전의 호환성을 위해 일부 오버라이딩된 메서드를 포함

  - 데이터베이스 이름을 사용하지 않고 db=0~16번까지 숫자를 이용하여 db를 구분

    - redis.conf 파일을 통해 변경 가능

------

### Redis를 이용한 게시물 열람 수 확인

- ORM을 이용하여 열람 수를 데이터베이스에 저장할 경우 사용자가 게시물을 화면에 띄울 때 마다 UPDATE를 사용하여 DB에 접근해야 한다.

- Redis를 이용할 경우 메모리에 열람 숫자만 저장하기 때문에 성능 향상을 가져올 수 있다.

  ```python
    def product_detail(request, id):
        product = get_object_or_404(Product, id=id)
    		redis_products = r.incr(f'product:{product.id}')
  ```

  - syntax - def incr(self, name, amount=1): 실행될 때 1(default)씩 증가

### 게시물 열람 순위

```python
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    redis_products = r.incr(f'product:{product.id}')
    # def zincrby(self, name, amount, value):
		# -> product_ranking을 키로 갖는 sorted set에 있는 value(id에 해당하는)의 score가 amount(1) 
		# 만큼 증가 
    r.zincrby('product_ranking', 1, product.id)
    return render(request, 'index.html')

def product_ranking(request):
    # 0-lowest, 1-highest
    product_ranking = r.zrange('product_ranking', 0, -1, desc=True)[:10]
    # print(r.zrangebyscore('product_ranking', 0, 100, withscores=True))
    # # [(b'14', 1.0), (b'13', 5.0), (b'11', 11.0)]
    product_ranking_ids = [int(id) for id in product_ranking]
    best_seller = list(Product.objects.filter(id__in=product_ranking_ids))
    best_seller.sort(key=lambda x: product_ranking_ids.index(x.id))
    return render(request, 'ranking.html')
```

- zincrby: key에 속한 value의 score로 정렬되기 때문에 리스트의 순위를 매길때 많이 사용된다.
- zrange(): score가 높은 순서대로 values를 담은 list를 반환

------

### Redis Architecture

[Redis Overview](http://redisgate.kr/redis/configuration/redis_overview.php)

- 주 저장장치 - main memory 
  - 메모리의 올라가 있는 데이터를 영구 보관을 위해 디스크에 저장할 수 있다.
  - RDB(Snapshot): 특정 시점에 메모리에 있는 데이터를 디스크에 저장 
    - process를 fork하기 때문에 원래의 process에 영향을 미치지 않지만, 디스크에 대한 I/O 작업 및  I/O에 대한 CPU의 block 상태가 자주 발생할 수 있다([**CPU process**](https://www.notion.so/afmadadans/Fast-Campus-3-26-94a8fabf9f5946d98d5203823b5419c6#24af225cd002413287fc1739cb383656)).
  - AOF(Append Only File): 조회를 제외한 입력/수정/삭제 동작이 이루어질 때 디스크에 저장 
    - 몇 가지 옵션이 있지만 그중 'everysec'를 주로 권장하며 1초마다 별도의 스레드가 데이터를 저장하기 때문에 메인 스레드에 영향을 주지 않고, 데이터 유실 최소화하면서 성능을 보장한다.
    - no: OS에 의해 저장 시점 결정(최대 30초)
    - always: 레디스 명령이 실행 될 때 마다 디스크 저장(성능이 낮음)

### Redis 기본 명령어

Delete all keys from all Redis databases:

```
$ redis-cli FLUSHALL
```

Delete all keys of the currently selected Redis database:

```
$ redis-cli FLUSHDB
```

Delete all keys of the specified Redis database:

```
$ redis-cli -n <database_number> FLUSHDB
```

[Redis: Delete All Keys - Redis-CLI - ShellHacks](https://www.shellhacks.com/redis-delete-all-keys-redis-cli/)

**타입에 따른 데이터 로드**

Here are the commands to retrieve key value:

- if value is of type string -> GET 

- if value is of type hash -> HGETALL

- if value is of type lists -> lrange

- if value is of type sets -> smembers

- if value is of type sorted sets -> ZRANGEBYSCORE

  ```python
    127.0.0.1:6379> ZRANGEBYSCORE image_ranking -inf +inf withscores
    1) "14"
    2) "1"
    3) "13"
    4) "5"
    5) "11"
    6) "11"
  ```

### EC2에 redis setting - from  [마이구미](https://mygumi.tistory.com/133)

```python
# download directory
sudo wget <http://download.redis.io/redis-stable.tar.gz>
sudo tar xvzf redis-stable.tar.gz
cd redis-stable
make

# ../redis-stable
sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/
# 또는
sudo make install
sudo mkdir -p /etc/redis /var/lib/redis /var/redis/6379
sudo cp redis.conf /etc/redis/6379.conf

sudo vim /etc/redis/6379.conf
# 아래의 내용 변경
---------------------------------------
bind 127.0.0.1
daemonize no
# append only file(AOF) Mode 설정
appendonly yes
appendfsync no  # always / everysec

---------------------------------------

logfile /var/log/redis_6379.log
dir /var/redis/6379

# initscript 설치
sudo wget <https://raw.githubusercontent.com/saxenap/install-redis-amazon-linux-centos/master/redis-server>
sudo mv redis-server /etc/init.d
sudo chmod 755 /etc/init.d/redis-server


sudo vi /etc/init.d/redis-server
# 아래의 내용 변경
REDIS_CONF_FILE="/etc/redis/6379.conf"

# 시작프로그램 추가, 런레벨 등록
update-rc.d redis-server defaults
update-rc.d redis-server start 20 3 4 5
# 제거
update-rc.d -f redis-server remove
```



**command to check the type of value a key mapping to: type**

[WRONGTYPE Operation against a key holding the wrong kind of value php](https://stackoverflow.com/questions/37953019/wrongtype-operation-against-a-key-holding-the-wrong-kind-of-value-php)

**Redis Gate**

[redis introduction 레디스 소개](http://redisgate.kr/redis/introduction/redis_intro.php)

**Django - Redis**

[Django에서 Redis를 이용해 Caching하기](https://jupiny.com/2018/02/27/caching-using-redis-on-django/)

**Redis - Key**

[Redis key pattern 관련](https://sncap.tistory.com/553)

**Memcached vs Redis**

[[Cache\]Redis vs Memcached](https://americanopeople.tistory.com/148)

**Redis 참고**

[In memory dictionary Redis 소개](https://bcho.tistory.com/654)