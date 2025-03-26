import pytest
from decimal import Decimal
from .models import Order, OrderLineItem
from .forms import OrderForm
from products.models import Product, Category
from profiles.models import UserProfile


@pytest.mark.django_db
class TestOrder:
    @pytest.fixture
    def user_profile(self):
        return UserProfile.objects.create(
            user_id=1,
            default_full_name='Test User',
            default_email='test@example.com',
            default_phone_number='1234567890',
            default_street_address1='123 Test St',
            default_town_or_city='Test City',
            default_postcode='12345',
            default_country='US'
        )

    def test_create_order(self, user_profile):
        order = Order.objects.create(
            user_profile=user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            postcode='12345',
            country='US'
        )
        assert order.user_profile == user_profile
        assert order.full_name == 'Test User'
        assert order.email == 'test@example.com'
        assert order.phone_number == '1234567890'
        assert order.street_address1 == '123 Test St'
        assert order.town_or_city == 'Test City'
        assert order.postcode == '12345'
        assert order.country == 'US'
        assert order.order_number is not None
        assert len(order.order_number) == 32
        assert order.order_total == Decimal('0')
        assert order.delivery_cost == Decimal('0')
        assert order.grand_total == Decimal('0')

    def test_order_without_user_profile(self):
        order = Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            postcode='12345',
            country='US'
        )
        assert order.user_profile is None

    def test_order_update_total(self, user_profile):
        # Create a category and product
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            category=category,
            name='Test Product',
            description='Test Description',
            price=Decimal('10.00')
        )

        # Create order and line item
        order = Order.objects.create(
            user_profile=user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            postcode='12345',
            country='US'
        )

        OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=2
        )

        order.update_total()
        assert order.order_total == Decimal('20.00')
        assert order.delivery_cost == Decimal('2.00')  # 10% of order total
        assert order.grand_total == Decimal('22.00')

    def test_order_update_total_free_delivery(self, user_profile):
        # Create a category and product
        category = Category.objects.create(name='Test Category')
        product = Product.objects.create(
            category=category,
            name='Test Product',
            description='Test Description',
            price=Decimal('100.00')
        )

        # Create order and line item
        order = Order.objects.create(
            user_profile=user_profile,
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            postcode='12345',
            country='US'
        )

        OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=2
        )

        order.update_total()
        assert order.order_total == Decimal('200.00')
        assert order.delivery_cost == Decimal('0')  # Free delivery over threshold # noqa
        assert order.grand_total == Decimal('200.00')


@pytest.mark.django_db
class TestOrderLineItem:
    @pytest.fixture
    def order(self):
        return Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            street_address1='123 Test St',
            town_or_city='Test City',
            postcode='12345',
            country='US'
        )

    @pytest.fixture
    def product(self):
        category = Category.objects.create(name='Test Category')
        return Product.objects.create(
            category=category,
            name='Test Product',
            description='Test Description',
            price=Decimal('10.00')
        )

    def test_create_line_item(self, order, product):
        line_item = OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=2
        )
        assert line_item.order == order
        assert line_item.product == product
        assert line_item.quantity == 2
        assert line_item.lineitem_total == Decimal('20.00')
        expected_str = (
            f'SKU {product.sku} on order {order.order_number}'
        )
        assert str(line_item) == expected_str

    def test_line_item_with_size(self, order, product):
        line_item = OrderLineItem.objects.create(
            order=order,
            product=product,
            product_size='M',
            quantity=1
        )
        assert line_item.product_size == 'M'
        assert line_item.lineitem_total == Decimal('10.00')


class TestOrderForm:
    def test_order_form_fields(self):
        form = OrderForm()
        expected_fields = {
            'full_name', 'email', 'phone_number', 'street_address1',
            'street_address2', 'town_or_city', 'postcode', 'country', 'county'
        }
        assert set(form.fields.keys()) == expected_fields

    def test_order_form_placeholders(self):
        form = OrderForm()
        assert form.fields['full_name'].widget.attrs['placeholder'] == (
            'Full Name *'
        )
        assert form.fields['email'].widget.attrs['placeholder'] == (
            'Email Address *'
        )
        assert form.fields['street_address2'].widget.attrs['placeholder'] == (
            'Street Address 2'
        )
        assert form.fields['county'].widget.attrs['placeholder'] == 'County'

    def test_order_form_classes(self):
        form = OrderForm()
        for field in form.fields:
            assert form.fields[field].widget.attrs['class'] == (
                'stripe-style-input'
            )

    def test_order_form_labels(self):
        form = OrderForm()
        for field in form.fields:
            assert form.fields[field].label is False

    def test_order_form_autofocus(self):
        form = OrderForm()
        assert form.fields['full_name'].widget.attrs['autofocus'] is True
        for field in form.fields:
            if field != 'full_name':
                assert 'autofocus' not in form.fields[field].widget.attrs
