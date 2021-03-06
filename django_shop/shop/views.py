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
    except Exception as e:
        suggested_items = None
        print(f'not connect redis:{e}')
    product_images = list()
    # product_images = ProductImage.objects.select_related('product').filter(product__in=suggested_items)
    try:
        for suggested_item in suggested_items:
            product_image = ProductImage.objects.select_related('product').get(product=suggested_item)
            product_images.append(product_image)
    except:
        pass
    categories = Category.objects.prefetch_related('subcategory_set').all()

    data = dict()
    for cat in categories:
        data[cat] = cat.subcategory_set.all()
    return render(request, template_name='shop/main.html',
                  context={'data': data, 'suggested_items': suggested_items, 'product_images': product_images})


def product_list(request, category_slug=None):
    q = request.GET.get('q')
    product_image = None
    category = None
    if q:
        # products = Product.objects.filter(name__icontains=q)
        product_image = ProductImage.objects.select_related('product').filter(product__name__icontains=q)
    elif category_slug:
        category = SubCategory.objects.get(slug=category_slug)
        product_image = ProductImage.objects.select_related('product').filter(product__category=category)

    return render(request, 'shop/product/list.html',
                  {'category': category, 'product_image': product_image})


def product_detail(request, p_id):
    product_image = ProductImage.objects.select_related('product').get(product__id=p_id)
    cart_form = CartForm()
    r = Recommend()
    try:
        suggested_items = r.suggest_items(product_id=p_id)[:3]
    except Exception as e:
        suggested_items = None
        print(f'not connect redis:{e}')
    return render(request, 'shop/product/detail.html',
                  {'product_image': product_image, 'cart_form': cart_form, 'suggested_items': suggested_items})
