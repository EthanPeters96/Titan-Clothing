import pytest
from decimal import Decimal
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from products.models import Product, Category
from .views import view_bag, add_to_bag, adjust_bag, remove_from_bag
from .contexts import bag_contents


@pytest.mark.django_db
class TestBagViews:
    @pytest.fixture
    def product(self):
        category = Category.objects.create(name='Test Category')
        return Product.objects.create(
            category=category,
            name='Test Product',
            description='Test Description',
            price=Decimal('10.00')
        )

    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    @pytest.fixture
    def request_with_session(self, request_factory):
        request = request_factory.get('/')
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_view_bag(self, request_with_session):
        response = view_bag(request_with_session)
        assert response.status_code == 200
        assert 'bag/bag.html' in [t.name for t in response.templates]

    def test_add_to_bag(self, request_with_session, product):
        request = request_with_session
        request.method = 'POST'
        request.POST = {'quantity': 2, 'redirect_url': reverse('view_bag')}
        response = add_to_bag(request, product.id)
        assert response.status_code == 302
        assert response.url == reverse('view_bag')
        assert request.session['bag'] == {str(product.id): 2}

        # Test adding same product again
        response = add_to_bag(request, product.id)
        assert request.session['bag'] == {str(product.id): 4}

        # Test adding product with size
        request.POST = {
            'quantity': 1,
            'product_size': 'M',
            'redirect_url': reverse('view_bag')
        }
        response = add_to_bag(request, product.id)
        assert str(product.id) in request.session['bag']
        assert 'items_by_size' in request.session['bag'][str(product.id)]
        assert (
            request.session['bag'][str(product.id)]['items_by_size']['M'] == 1
        )

    def test_adjust_bag(self, request_with_session, product):
        request = request_with_session
        # First add an item
        request.method = 'POST'
        request.POST = {'quantity': 2, 'redirect_url': reverse('view_bag')}
        add_to_bag(request, product.id)

        # Then adjust it
        request.POST = {'quantity': 3}
        response = adjust_bag(request, product.id)
        assert response.status_code == 302
        assert response.url == reverse('view_bag')
        assert request.session['bag'] == {str(product.id): 3}

        # Test removing item by setting quantity to 0
        request.POST = {'quantity': 0}
        response = adjust_bag(request, product.id)
        assert str(product.id) not in request.session['bag']

        # Test adjusting product with size
        request.POST = {
            'quantity': 1,
            'product_size': 'M',
            'redirect_url': reverse('view_bag')
        }
        add_to_bag(request, product.id)

        request.POST = {'quantity': 2, 'product_size': 'M'}
        response = adjust_bag(request, product.id)
        assert (
            request.session['bag'][str(product.id)]['items_by_size']['M'] == 2
        )

    def test_remove_from_bag(self, request_with_session, product):
        request = request_with_session
        # First add an item
        request.method = 'POST'
        request.POST = {'quantity': 2, 'redirect_url': reverse('view_bag')}
        add_to_bag(request, product.id)

        # Then remove it
        request.method = 'POST'
        request.POST = {}
        response = remove_from_bag(request, product.id)
        assert response.status_code == 200
        assert str(product.id) not in request.session['bag']

        # Test removing product with size
        request.POST = {
            'quantity': 1,
            'product_size': 'M',
            'redirect_url': reverse('view_bag')
        }
        add_to_bag(request, product.id)

        request.POST = {'product_size': 'M'}
        response = remove_from_bag(request, product.id)
        assert response.status_code == 200
        assert str(product.id) not in request.session['bag']


@pytest.mark.django_db
class TestBagContext:
    @pytest.fixture
    def product(self):
        category = Category.objects.create(name='Test Category')
        return Product.objects.create(
            category=category,
            name='Test Product',
            description='Test Description',
            price=Decimal('10.00')
        )

    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    @pytest.fixture
    def request_with_session(self, request_factory):
        request = request_factory.get('/')
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        return request

    def test_bag_contents_empty(self, request_with_session):
        context = bag_contents(request_with_session)
        assert context['bag_items'] == []
        assert context['total'] == 0
        assert context['product_count'] == 0
        assert context['delivery'] == 0
        assert context['free_delivery_delta'] == 0
        assert context['grand_total'] == 0

    def test_bag_contents_with_items(self, request_with_session, product):
        request = request_with_session
        request.session['bag'] = {str(product.id): 2}
        request.session.save()
        context = bag_contents(request)
        assert len(context['bag_items']) == 1
        assert context['total'] == Decimal('20.00')
        assert context['product_count'] == 2
        assert context['grand_total'] == Decimal('22.00')  # Including delivery

    def test_bag_contents_with_sizes(self, request_with_session, product):
        request = request_with_session
        request.session['bag'] = {
            str(product.id): {'items_by_size': {'M': 2, 'L': 1}}
        }
        request.session.save()
        context = bag_contents(request)
        assert len(context['bag_items']) == 2
        assert context['total'] == Decimal('30.00')
        assert context['product_count'] == 3
        assert context['grand_total'] == Decimal('33.00')  # Including delivery

    def test_bag_contents_free_delivery(self, request_with_session, product):
        request = request_with_session
        request.session['bag'] = {str(product.id): 20}  # 20 items = $200
        request.session.save()
        context = bag_contents(request)
        assert context['delivery'] == 0
        assert context['grand_total'] == Decimal('200.00')
