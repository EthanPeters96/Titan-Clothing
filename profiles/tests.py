import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from .models import UserProfile
from .forms import (
    UserProfileForm, SuperUserForm, SuperUserEditForm,
    ProductForm, CategoryForm
)
from products.models import Category


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def test_profile(test_user):
    return UserProfile.objects.get_or_create(user=test_user)[0]


class TestUserProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_profile_creation(self):
        """Test that a profile is created when a user is created"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.user.email, 'test@example.com')

    def test_profile_str_method(self):
        """Test the string representation of a profile"""
        self.assertEqual(str(self.profile), 'testuser')


class TestUserProfileForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.get(user=self.user)

    def test_user_profile_form_fields(self):
        form = UserProfileForm()
        expected_fields = [
            'default_full_name',
            'default_email',
            'default_phone_number',
            'default_street_address1',
            'default_street_address2',
            'default_town_or_city',
            'default_county',
            'default_postcode',
            'default_country',
        ]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_user_profile_form_placeholders(self):
        form = UserProfileForm()
        expected_placeholders = {
            'default_full_name': 'Full Name',
            'default_email': 'Email Address',
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County',
            'default_postcode': 'Postal Code',
        }
        for field, placeholder in expected_placeholders.items():
            self.assertEqual(
                form.fields[field].widget.attrs['placeholder'],
                placeholder
            )

    def test_user_profile_form_classes(self):
        form = UserProfileForm()
        for field in form.fields:
            self.assertEqual(
                form.fields[field].widget.attrs['class'],
                'border-black rounded-0 profile-form-input'
            )

    def test_user_profile_form_labels(self):
        form = UserProfileForm()
        for field in form.fields:
            self.assertFalse(form.fields[field].label)

    def test_user_profile_form_autofocus(self):
        form = UserProfileForm()
        self.assertTrue(
            form.fields['default_full_name'].widget.attrs.get('autofocus')
        )


@pytest.mark.django_db
class TestSuperUserForm:
    def test_superuser_form_fields(self):
        form = SuperUserForm()
        expected_fields = {'username', 'email', 'password1', 'password2'}
        assert set(form.fields.keys()) == expected_fields

    def test_superuser_form_classes(self):
        form = SuperUserForm()
        for field in form.fields:
            assert form.fields[field].widget.attrs['class'] == (
                'border-black rounded-0'
            )

    def test_superuser_form_save(self):
        form_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password1': 'adminpass123',
            'password2': 'adminpass123'
        }
        form = SuperUserForm(form_data)
        assert form.is_valid()
        user = form.save()
        assert user.is_superuser is True
        assert user.is_staff is True
        assert user.username == 'admin'
        assert user.email == 'admin@example.com'


@pytest.mark.django_db
class TestSuperUserEditForm:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_superuser_edit_form_fields(self):
        form = SuperUserEditForm()
        expected_fields = {'username', 'email', 'is_active'}
        assert set(form.fields.keys()) == expected_fields

    def test_superuser_edit_form_classes(self):
        form = SuperUserEditForm()
        for field in form.fields:
            assert form.fields[field].widget.attrs['class'] == (
                'border-black rounded-0'
            )

    def test_superuser_edit_form_save(self, user):
        form_data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'is_active': True
        }
        form = SuperUserEditForm(form_data, instance=user)
        assert form.is_valid()
        updated_user = form.save()
        assert updated_user.username == 'newusername'
        assert updated_user.email == 'newemail@example.com'
        assert updated_user.is_active is True


@pytest.mark.django_db
class TestProductForm:
    @pytest.fixture
    def category(self):
        return Category.objects.create(
            name='test_category',
            friendly_name='Test Category'
        )

    def test_product_form_fields(self, category):
        form = ProductForm()
        expected_fields = {
            'category', 'sku', 'name', 'description', 'has_sizes',
            'price', 'rating', 'image_url', 'image'
        }
        assert set(form.fields.keys()) == expected_fields

    def test_product_form_labels(self, category):
        form = ProductForm()
        assert form.fields['sku'].label == 'SKU (Stock Keeping Unit)'
        assert form.fields['name'].label == 'Product Name'
        assert form.fields['description'].label == 'Product Description'
        assert form.fields['has_sizes'].label == 'Has Different Sizes?'
        assert form.fields['price'].label == 'Price (£)'
        assert form.fields['rating'].label == 'Rating (0-5)'
        assert form.fields['image_url'].label == 'Image URL (optional)'
        assert form.fields['image'].label == 'Upload Image (optional)'

    def test_product_form_classes(self, category):
        form = ProductForm()
        for field in form.fields:
            assert form.fields[field].widget.attrs['class'] == (
                'border-black rounded-0'
            )

    def test_product_form_category_choices(self, category):
        form = ProductForm()
        assert (category.id, category.get_friendly_name()) in (
            form.fields['category'].choices
        )


@pytest.mark.django_db
class TestCategoryForm:
    def test_category_form_fields(self):
        form = CategoryForm()
        expected_fields = {'name', 'friendly_name', 'group'}
        assert set(form.fields.keys()) == expected_fields

    def test_category_form_help_texts(self):
        form = CategoryForm()
        assert form.fields['name'].help_text == (
            'URL/filtering name (lowercase, no spaces)'
        )
        assert form.fields['friendly_name'].help_text == (
            'Display name for customers'
        )
        assert form.fields['group'].help_text == (
            'Navigation group (e.g., Clothing, Accessories)'
        )

    def test_category_form_classes(self):
        form = CategoryForm()
        for field in form.fields:
            assert form.fields[field].widget.attrs['class'] == (
                'border-black rounded-0'
            )
