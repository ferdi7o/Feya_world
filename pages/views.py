from django.views.generic import ListView
from products.models import Product


class HomeView(ListView):
    model = Product
    template_name = 'pages/home.html'
    context_object_name = 'latest_products'

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')[:6]