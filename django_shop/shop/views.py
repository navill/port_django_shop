from django.shortcuts import get_object_or_404, render

# Create your views here.
from cart.forms import CartForm
from shop.models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    # product list에서 category를 선택했을 경우
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html',
                  {'categories': categories, 'category': category, 'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart_form = CartForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_form': cart_form})
