import itertools
import time
from functools import wraps
from memory_profiler import profile


def benchmarker_time(org_func):
    @wraps(org_func)
    def inner(*args, **kwargs):
        start = time.time()
        result = org_func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000
        print(f'elapsed time with timer decorator : {elapsed:.5f}ms')
        return result

    return inner


product_ids = range(100)
print(product_ids)
for i in product_ids:
    print(i)


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
    # 조합 생성 - 순서를 상관하지않고 중복을 허용하지 않음
    li = itertools.combinations(product_ids, len(product_ids) - 1)
    for item2 in li:
        # a = list(map(lambda x:x*2, product_ids))
        item = set(product_ids) - set(item2)
        result = list(map(lambda item: item, item2))
        print(result)


# func_a(product_ids)
# func_b(product_ids)

li = ['a', 'b', 'c']
iter_li = itertools.combinations(li, len(li)-1)
print(iter_li)
for i in iter_li:
    print(i)
