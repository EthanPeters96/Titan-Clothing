from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from products.models import Product, Category
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_county': 'County',
            'default_postcode': 'Postal Code',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0 profile-form-input' # noqa
            self.fields[field].label = False


class SuperUserForm(UserCreationForm):
    """Form to create a new superuser"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = True
        user.is_staff = True
        if commit:
            user.save()
        return user


class SuperUserEditForm(forms.ModelForm):
    """Form to edit an existing superuser"""
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'border-black rounded-0'


class ProductForm(forms.ModelForm):
    """Form to add or edit a product"""
    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image', required=False,
        widget=forms.FileInput()
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        help_text='Provide a detailed description of the product'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names

        # Add clear labels to help users understand what each field needs
        self.fields['sku'].label = 'SKU (Stock Keeping Unit)'
        self.fields['name'].label = 'Product Name'
        self.fields['description'].label = 'Product Description'
        self.fields['has_sizes'].label = 'Has Different Sizes?'
        self.fields['price'].label = 'Price (£)'
        self.fields['rating'].label = 'Rating (0-5)'
        self.fields['image_url'].label = 'Image URL (optional)'
        self.fields['image'].label = 'Upload Image (optional)'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class CategoryForm(forms.ModelForm):
    """Form to add or edit a category"""
    class Meta:
        model = Category
        fields = ['name', 'friendly_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
