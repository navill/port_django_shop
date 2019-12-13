class Singleton:
    _instance = None

    # Cart의 경우 입력된 매개변수(request)가 반영되어야 한다.
    # request를 요청한 사용자마다 다른 request.session을 사용해야 한다.
    def __new__(cls, *args, **kwargs):
        # Cart의 객체인지 확인
        # 아래 조건문이 True 경우, 새로운 cls._instance 생성 후 반환, False일 경우 None 반환
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance
