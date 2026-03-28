from django.urls import path
from .api_views import ProductListAPIView
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('api/list/', ProductListAPIView.as_view(), name='api_product_list'),
]