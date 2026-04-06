from django.views.generic import ListView, TemplateView
from products.models import Product


class HomeView(ListView):
    model = Product
    template_name = 'pages/home.html'
    context_object_name = 'latest_products'

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')[:6]

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'