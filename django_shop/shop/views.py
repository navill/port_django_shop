from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render

# Create your views here.
from cart.forms import CartForm
from shop.models import Category, Product


def product_list(request, category_slug=None):
    category = None
    category_all = Category.objects.all()
    product_all = Product.objects.all()
    # cache.get
    products = cache.get('products')
    categories = cache.get('categories')

    # cache.set
    # 기존의 코드 -> 첫 페이지 로드 시, products가 None을 반환하기 때문에
    # 두 번 연속(캐쉬가 리셋되기 전) 페이지를 로드 해야 제품 리스트가 표시되는 문제
    # => 아래와 같이 QuerySet의 인스턴스인지 여부를 확인하여 cache.get/set 처리
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
            if category_slug == cat.slug:
                category = cat
        products = products.filter(category=category)
    paginator = Paginator(products, 6)
    products = paginator.get_page(page)
    return render(request, 'shop/product/list.html',
                  {'categories': categories, 'category': category, 'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart_form = CartForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_form': cart_form})
