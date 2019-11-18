import redis
from django.conf import settings

from shop.models import Product

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class Recommend:
    def buy_item(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            r.zincrby('product', value=product_id, amount=1)
            # 주 아이템(product_id) + 함께 구매한 아이템(with_id)
            for with_id in product_ids:
                # product_id + product_id를 피하기 위한 조건문
                if product_id != with_id:
                    # key[product:1(product_id)] : value[2(with_id - score:1(amount 만큼 증가))]
                    r.zincrby(f'product:{product_id}', value=with_id, amount=1)

    def suggest_items(self, product_id=None):
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
