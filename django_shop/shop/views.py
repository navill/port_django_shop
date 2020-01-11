from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render

# Create your views here.
from cart.forms import CartForm
from shop.models import Category, Product, SubCategory, ProductImage
from shop.recommender import Recommend


def home(request):
    r = Recommend()
    # suggested_items = r.suggest_items()
    try:
        suggested_items = r.suggest_items()
        print(suggested_items)
    except Exception as e:
        suggested_items = None
        print(f'not connect redis:{e}')

    data = dict()

    categories = Category.objects.prefetch_related('subcategory_set').all()

    # product_id_list = [p.id for p in suggested_items]
    # suggested_items = Product.objects.prefetch_related('product_image').filter(id__in=product_id_list)

    for cat in categories:
        data[cat] = cat.subcategory_set.all()
    return render(request, template_name='shop/main.html',
                  context={'data': data, 'suggested_items': suggested_items})


def product_list(request, category_slug=None):
    """
    Cache - 보류

    category = None
    category_all = Category.objects.all()
    product_all = Product.objects.all()
    # cache.get
    products = cache.get('products')
    categories = cache.get('categories')

    # cache.set
    if not isinstance(products, QuerySet) and not isinstance(categories, QuerySet):  # 또는 그냥 if products is None:
        cache.set('products', product_all, 300)
        cache.set('categories', category_all, 300)
        products = cache.get('products')
        categories = cache.get('categories')
        # 만일 memcached가 동작하지 않을 경우
        if products is None:
            products = product_all
            categories = category_all
    """
    cart_form = CartForm()
    page = request.GET.get('page')
    # products = Product.objects.all()
    # product list에서 category를 선택했을 경우

    category = None
    if category_slug:
        category = SubCategory.objects.get(slug=category_slug)
        product_image = ProductImage.objects.select_related('product').filter(product__category=category)
        products = [pi.product for pi in product_image]
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 6)
    products = paginator.get_page(page)
    r = Recommend()
    try:
        suggested_items = r.suggest_items()
    except Exception as e:
        suggested_items = None
        print(f'not connect redis:{e}')
    return render(request, 'shop/product/list.html',
                  {'category': category, 'products': products,
                   'suggested_items': suggested_items})


def product_detail(request, p_id):
    product = get_object_or_404(Product, id=p_id)
    cart_form = CartForm()
    r = Recommend()
    try:
        suggested_items = r.suggest_items(product_id=p_id)
    except Exception as e:
        suggested_items = None
        print(f'not connect redis:{e}')
    return render(request, 'shop/product/detail.html',
                  {'product': product, 'cart_form': cart_form, 'suggested_items': suggested_items})
