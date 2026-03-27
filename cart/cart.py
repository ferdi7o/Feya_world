from decimal import Decimal
from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, size=None):
        product_id = str(product.id)
        # Beden seçimi varsa anahtara ekleyelim (Örn: "5-XL")
        item_key = f"{product_id}-{size}" if size else product_id

        if item_key not in self.cart:
            self.cart[item_key] = {
                'quantity': 0,
                'price': str(product.price),
                'size': size,
                'product_id': product_id
            }
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