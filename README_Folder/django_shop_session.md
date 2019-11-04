[How to use sessions | Django documentation | Django](https://docs.djangoproject.com/en/2.2/topics/http/sessions/#extending-database-backed-session-engines)

### Django Session Framework

- Session engine을 사용하기 위해 [settings.py](http://settings.py/)의 MIDDLEWARE에 'django.contrib.sessions.middleware.SessionMiddleware'를 포함해야 한다(default).
- session은 익명(anonymous) 세션과 인증(authenticated) 세션으로 구분된다.
  - 온라인 샵 구현 시, 로그인 전에 담아 두었던 장바구니는 로그인하는 순간 삭제되고 인증 세션이 새로 생성되므로 필요할 경우 반드시 익명 세션을 인증 세션으로 복사하는 로직을 구현해야 한다.

## Setting Session

- Session의 저장 방식에 따라 SESSION_ENGINE을 설정해야 한다.

  - Database session(default): 세션을 데이터베이스에 저장한다.

    - 별도의 세션 엔진을 설정하지 않아도 됨 → 프로젝트 생성 시 포함

  - File-based session("django.contrib.sessions.backends.file")

    - 세션을 파일 시스템에 저장한다.

  - Cached session("django.contrib.sessions.backends.cache")

    - cache backend에 세션을 저장한다.
    - CACHES 설정을 통해 cache backend를 설정할 수 있다.
    - 가장 높은 성능을 발휘한다.
    - Redis나 다른 cache 시스템을 위한 third-party backend를 이용할 수 있다.

  - Cached database session("django.contrib.sessions.backends.cached_db")

    - 세션 데이터를 [write-through](http://melonicedlatte.com/computerarchitecture/2019/02/12/203749.html) 방식으로 저장

      → 세션에 데이터를 저장할 때 캐쉬와 데이터베이스 모두에 데이터를 저장

    - 데이터가 캐시에 없을 경우, 데이터베이스에 있는 데이터를 이용한다.(read-only)

  - Cookie-based session("django.contrib.sessions.backends.signed_cookies")

    - 세션 데이터를 브라우저에 전송할 쿠키에 저장한다.

- customizing session을 위해 아래와 같은 옵션을 설정할 수 있다.

  - SESSION_COOKIE_AGE: 초 단위(default:1209600-2주)로 세션을 유지할 기간을 지정
  - SESSION_COOKIE_DOMAIN: 세션을 이용할 도메인 지정
  - SESSION_COOKIE_SECURE: HTTPS에서만 세션 쿠키를 이용
  - SESSION_EXPIRE_AT_BROWSER_CLOSE: 브라우저를 닫았을 때, 쿠키를 만료시킴
  - SESSION_SAVE_EVERY_REQUEST: 매 request 마다 세션을 데이터베이스에 저장
    - 업데이트 될 때 마다 만료 기간은 갱신된다.
