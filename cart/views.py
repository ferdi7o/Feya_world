from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, ProductVariant
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))

    variant_id = request.POST.get('variant_id')
    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, id=variant_id)

    cart.add(product=product, quantity=quantity, variant=variant)

    return redirect('cart_detail')


def cart_remove(request, item_key):
    cart = Cart(request)
    cart.remove(item_key)
    return redirect('cart_detail')