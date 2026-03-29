from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVariant, Review

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'product_type', 'category', 'is_shipping_free')
    list_filter = ('product_type', 'category', 'is_shipping_free')
    search_fields = ('title', 'description')
    inlines = [ProductImageInline, ProductVariantInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Review)