from django.urls import path
from .views import OrderCreateView, OrderListView, ModeratorOrderListView, OrderStatusUpdateView, OrderDetailView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('my-orders/', OrderListView.as_view(), name='order_list'),
    path('moderator-panel/', ModeratorOrderListView.as_view(), name='moderator_order_list'),
    path('status-update/<int:pk>/', OrderStatusUpdateView.as_view(), name='order_status_update'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]