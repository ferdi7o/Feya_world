from decimal import Decimal

from django.utils.timezone import override

from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, variant=None, override_quantity=False):
        product_id = str(product.id)

        item_key = f"{product_id}-{variant.id}" if variant else product_id

        if item_key not in self.cart:
            self.cart[item_key] = {
                'quantity': 0,
                'price': str(product.price),
                'variant_id': variant.id if variant else None,
                'product_id': product_id
            }

        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for item_key, item in self.cart.items():
            product = Product.objects.get(id=item['product_id'])
            item['product'] = product
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()