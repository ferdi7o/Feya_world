from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from .models import Product, Review, ProductImage, Category
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import ReviewForm, ProductForm, ProductVariantFormSet
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['variants'] = ProductVariantFormSet(self.request.POST)
        else:
            context['variants'] = ProductVariantFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        variants = context['variants']

        if form.is_valid() and variants.is_valid():
            self.object = form.save()

            images = self.request.FILES.getlist('images')
            for img in images:
                ProductImage.objects.create(product=self.object, image=img)

            variants.instance = self.object
            variants.save()

            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        return self.request.user.is_moderator


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'  # CreateView ile aynı template'i kullanabiliriz

    def test_func(self):
        return self.request.user.is_moderator

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(product=self.object, image=img)
        return response


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category = Category.objects.filter(slug__iexact=category_slug).first()
            if category:
                return queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            context['category'] = Category.objects.filter(slug__iexact=category_slug).first()

        return context