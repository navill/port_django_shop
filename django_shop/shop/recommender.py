import itertools
from functools import partial

import redis
from django.conf import settings

from shop.models import Product
from shop.pattern_singleton import Singleton

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommend(Singleton):
    def __init__(self):
        self.connect_status = False

    # @benchmarker_time
    # @profile(precision=10)
    def buy_item(self, products):
        if self.connect_status:
            product_ids = [p.id for p in products]
            # 이중 for -> 4.67682ms
            # for product_id in product_ids:
            #     r.zincrby('product', value=product_id, amount=1)
            #     # 주 아이템(product_id) + 함께 구매한 아이템(with_id)
            #     for with_id in product_ids:
            #         # product_id + product_id를 피하기 위한 조건문
            #         # -> A, B, C를 함께 구매할 경우 A,B & A,C만 해당, A,A는 제외되어야 한다.
            #         if product_id != with_id:
            #             # key[product:1(product_id)] : value[2(with_id - score:1(amount 만큼 증가))]
            #             r.zincrby(f'product:{product_id}', value=with_id, amount=1)

            # 순열 조합 생성 -> 3.83997ms
            com_ids = itertools.combinations(product_ids, len(product_ids) - 1)

            for ids in com_ids:
                product_id = list(set(product_ids) - set(ids))
                # product_ids와 순열 조합의 크기는 1만큼 차이나기때문에 항상 len(product_id)는 1이다
                product_id = int(product_id[0])
                # value를 제외한 인수 고정
                # c_zincrby = partial(custom_zincrby, name=f'product:{product_id}', amount=1)
                # r.zincrby('product', value=product_id, amount=1)
                # # list로 감싸지 않으면 c_zincrby 동작 x
                # list(map(c_zincrby, ids))
                partial_zincrby = partial(r.zincrby, name=f'product:{product_id}', amount=1)
                list(map(lambda value: partial_zincrby(value=value), ids))

    def suggest_items(self, product_id=None):
        if self.connect_status:
            # in product_detail
            if product_id:
                items = r.zrange(f'product:{product_id}', 0, -1, desc=True)[:3]
            # in product_list
            else:
                items = r.zrange('product', 0, -1, desc=True)[:3]
            item_ids = [int(item_id) for item_id in items]
            best_items = list(Product.objects.filter(id__in=item_ids))
            # item_ids 순서에 맞게 product object 정렬
            best_items.sort(key=lambda b: item_ids.index(b.id))
            return best_items
