from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from .models import Product, Review
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ReviewForm, ProductForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)

        if not request.user.is_authenticated:
            messages.error(request, "Трябва да сте влезли в профила си, за да оставите коментар.")
            return redirect('login')

        if form.is_valid():
            # Kullanıcının daha önce yorum yapıp yapmadığını kontrol et (Ödev kuralı)
            if Review.objects.filter(product=self.object, user=request.user).exists():
                messages.warning(request, "Вече сте дали оценка за този продукт.")
            else:
                review = form.save(commit=False)
                review.product = self.object
                review.user = request.user
                review.save()
                messages.success(request, "Благодарим ви за вашата оценка!")
            return redirect('product_detail', pk=self.object.pk)

        return self.render_to_response(self.get_context_data(review_form=form))


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        return self.request.user.is_moderator

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        return self.request.user.is_moderator
