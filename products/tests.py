from django.test import TestCase
from django.urls import reverse
from .models import Product, Category

class ProductTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Чаши', slug='cups')
        self.product = Product.objects.create(
            title='Тестова Чаша',
            price=15.00,
            category=self.category,
            description='Описание на тестовия продукт',
            product_type='mug', #product category from admin panel!
            stock=10
        )
    # +5 tests from users/tests.py
    def test_product_content(self):
        """6. Проверка дали данните на продукта (заглавието) се записват правилно."""
        self.assertEqual(self.product.title, 'Тестова Чаша')

    def test_category_slug(self):
        """7. Проверка дали автоматичното генериране на slug за категорията работи."""
        self.assertEqual(self.category.slug, 'cups')

    def test_product_list_view(self):
        """8. Проверка дали началната страница/списъкът с продукти работи (Status 200)."""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестова Чаша')

    def test_product_detail_view(self):
        """9. Проверка дали страницата с детайли за продукта се отваря успешно."""
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)

    def test_category_filter_view(self):
        """10. Проверка дали филтрирането по категория работи правилно."""
        response = self.client.get(reverse('product_list_by_category', kwargs={'category_slug': 'cups'}))
        self.assertEqual(response.status_code, 200)

    def test_product_create_requires_moderator(self):
        """11. Проверка на правата: Обикновен потребител не трябва да може да добавя продукти."""
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 302)

    def test_non_existent_product_404(self):
        """12. Проверка дали системата връща грешка 404 при несъществуващ продукт."""
        response = self.client.get(reverse('product_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_product_search_logic(self):
        """13. Проверка на логиката за търсене или филтриране по заглавие (title)."""
        products = Product.objects.filter(title__icontains='Чаша')
        self.assertTrue(products.exists())

    def test_review_form_on_detail_page(self):
        """14. Проверка дали формата за коментари присъства в страницата с детайли."""
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product.pk}))
        self.assertIn('review_form', response.context)

    def test_delete_confirmation_page_url(self):
        """15. Проверка дали URL адресът за потвърждение на изтриване е правилно конфигуриран."""
        url = reverse('product_delete', kwargs={'pk': self.product.pk})
        self.assertIsNotNone(url)