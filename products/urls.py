from django.urls import path

from . import views
from .api_views import ProductListAPIView
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('api/list/', ProductListAPIView.as_view(), name='api_product_list'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
]