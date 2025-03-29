import pytest
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Product
from .utils import clean_filename

# Create your tests here.


@pytest.mark.django_db
class TestCategory:
    def test_create_category(self):
        category = Category.objects.create(
            name='test_category',
            friendly_name='Test Category'
        )
        assert category.name == 'test_category'
        assert category.friendly_name == 'Test Category'
        assert str(category) == 'Test Category'

    def test_category_get_friendly_name(self):
        category = Category.objects.create(
            name='test_category',
            friendly_name='Test Category'
        )
        assert category.get_friendly_name() == 'Test Category'


@pytest.mark.django_db
class TestProduct:
    @pytest.fixture
    def category(self):
        return Category.objects.create(
            name='test_category',
            friendly_name='Test Category'
        )

    def test_create_product(self, category):
        product = Product.objects.create(
            category=category,
            name='Test Product',
            description='Test Description',
            price=Decimal('99.99')
        )
        assert product.category == category
        assert product.name == 'Test Product'
        assert product.description == 'Test Description'
        assert product.price == Decimal('99.99')
        assert str(product) == 'Test Product'

    def test_product_without_optional_fields(self):
        product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=Decimal("99.99")
        )
        assert product.sku is None
        assert product.has_sizes is False
        assert product.rating is None
        assert product.image_url is None
        assert product.image.name == ''  # Empty string for empty ImageField

    def test_product_with_all_fields(self, category):
        # Create a test image
        image_content = b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'  # noqa: E501
        image = SimpleUploadedFile(
            'test.gif',
            image_content,
            content_type='image/gif'
        )

        product = Product.objects.create(
            category=category,
            sku='TEST123',
            name='Test Product',
            description='Test Description',
            price=Decimal('99.99'),
            has_sizes=True,
            rating=4.5,
            image_url='https://example.com/image.jpg',
            image=image
        )
        assert product.category == category
        assert product.sku == 'TEST123'
        assert product.name == 'Test Product'
        assert product.description == 'Test Description'
        assert product.price == Decimal('99.99')
        assert product.has_sizes is True
        assert product.rating == 4.5
        assert product.image_url == 'https://example.com/image.jpg'
        assert product.image.name.endswith('.gif')


@pytest.mark.django_db
class TestCleanFilename:
    def test_clean_filename_with_spaces(self):
        assert clean_filename("test file.jpg") == "test-file.jpg"

    def test_clean_filename_with_special_chars(self):
        assert clean_filename("test@file.jpg") == "testfile.jpg"

    def test_clean_filename_with_multiple_extensions(self):
        assert clean_filename("test.file.jpg") == "testfile.jpg"

    def test_clean_filename_with_uppercase(self):
        assert clean_filename("TEST.JPG") == "test.jpg"

    def test_clean_filename_with_no_extension(self):
        assert clean_filename("testfile") == "testfile"
