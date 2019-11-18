from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render

# Create your views here.
from cart.forms import CartForm
from shop.models import Category, Product
from shop.recommender import Recommend


def product_list(request, category_slug=None):
    category = None
    category_all = Category.objects.all()
    product_all = Product.objects.all()
    # cache.get
    products = cache.get('products')
    categories = cache.get('categories')

    # cache.set
    if not isinstance(products, QuerySet):  # 또는 그냥 if products is None:
        cache.set('products', product_all, 300)
        products = cache.get('products')
    if not isinstance(categories, QuerySet):
        cache.set('categories', category_all, 300)
        categories = cache.get('categories')

    page = request.GET.get('page')
    # product list에서 category를 선택했을 경우
    if category_slug:
        # category = get_object_or_404(Category, slug=category_slug)
        # category = categories.get(slug=category_slug) -> get()에 의해 db 접근
        for cat in categories:
            if cat.slug == category_slug:
                category = cat
                break
        # raise query
        products = products.filter(category=category)
        # python 객체로 변환하여, 한 번의 db 접근으로 pagination 및 template에서 사용
        products = [product for product in products]
    paginator = Paginator(products, 6)
    products = paginator.get_page(page)
    r = Recommend()
    suggested_items = r.suggest_items()
    return render(request, 'shop/product/list.html',
                  {'categories': categories, 'category': category, 'products': products,
                   'suggested_items': suggested_items})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart_form = CartForm()
    r = Recommend()
    suggested_items = r.suggest_items(id)
    return render(request, 'shop/product/detail.html',
                  {'product': product, 'cart_form': cart_form, 'suggested_items': suggested_items})
