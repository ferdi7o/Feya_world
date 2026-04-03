from decimal import Decimal

from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.mixins import UserPassesTestMixin


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/order_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        total_price = cart.get_total_price()

        has_free_shipping_product = any(item['product'].is_shipping_free for item in cart)
        free_shipping_limit = Decimal('50.00')

        if has_free_shipping_product or total_price >= free_shipping_limit:
            shipping_cost = Decimal('0.00')
        else:
            shipping_cost = max((Decimal(str(item['product'].shipping_cost)) for item in cart), default=Decimal('0.00'))

        context['cart'] = cart
        context['shipping_cost'] = shipping_cost
        context['free_limit'] = free_shipping_limit
        context['remaining_for_free'] = free_shipping_limit - total_price
        context['grand_total'] = total_price + shipping_cost
        return context

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save(commit=False)
        order.user = self.request.user
        total_price = cart.get_total_price()

        has_free_shipping_product = any(item['product'].is_shipping_free for item in cart)
        free_shipping_limit = Decimal('50.00')

        if has_free_shipping_product or total_price >= free_shipping_limit:
            shipping = Decimal('0.00')
        else:
            shipping = max((Decimal(str(item['product'].shipping_cost)) for item in cart), default=Decimal('0.00'))

        order.shipping_cost = shipping
        order.total_paid = total_price + shipping
        order.save()

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
                size=item['variant'].size if item.get('variant') else "-"
            )

        cart.clear()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.id})

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


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)