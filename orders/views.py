from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.mixins import UserPassesTestMixin


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/order_create.html'

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save(commit=False)
        order.user = self.request.user

        total_price = cart.get_total_price()
        shipping = 10.00 if total_price < 100 else 0.00

        order.shipping_cost = shipping
        order.total_paid = total_price + shipping
        order.save()

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
                size=item.get('size')
            )

        cart.clear()
        return super().form_valid(form)

    def get_success_url(self):
        return f"/orders/status/{self.object.id}/"

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created')

class ModeratorOrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'orders/moderator_orders.html'
    context_object_name = 'all_orders'

    def test_func(self):
        return self.request.user.is_moderator or self.request.user.is_staff

class OrderStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['status']
    template_name = 'orders/order_status_update.html'
    success_url = '/orders/moderator-panel/'

    def test_func(self):
        return self.request.user.is_moderator