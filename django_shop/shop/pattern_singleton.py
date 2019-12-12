class Singleton:
    _instance = None

    def __new__(cls, *args):
        # Cart의 객체인지 확인
        # 아래 조건문이 True 경우, 새로운 cls._instance 생성 후 반환, False일 경우 None 반환
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance
