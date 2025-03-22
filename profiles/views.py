from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from checkout.models import Order
from products.models import Product, Category
from .models import UserProfile
from .forms import (
    UserProfileForm, SuperUserForm, SuperUserEditForm,
    ProductForm, CategoryForm
)


@login_required
def profile(request):
    """ Display the user's profile. """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create the profile if it doesn't exist
        profile = UserProfile.objects.create(user=request.user)
        messages.info(request, "Created a new profile for you.")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.') # noqa
    else:
        form = UserProfileForm(instance=profile)

    # Safely get orders - handle case where it might not exist yet
    try:
        orders = profile.orders.all().order_by('-date')
    except Exception:
        orders = []

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def add_superuser(request):
    """ Add a superuser """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    if request.method == 'POST':
        form = SuperUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added superuser!')
            return redirect('product_management')
        else:
            messages.error(
                request,
                'Failed to add superuser. Please ensure the form is valid.'
            )
    else:
        form = SuperUserForm()

    template = 'profiles/add_superuser.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_superuser(request, user_id):
    """ Edit a superuser """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    user = get_object_or_404(User, id=user_id, is_superuser=True)

    if request.method == 'POST':
        form = SuperUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated superuser!')
            return redirect('product_management')
        else:
            messages.error(
                request,
                'Failed to update superuser. Please ensure the form is valid.'
            )
    else:
        form = SuperUserEditForm(instance=user)

    template = 'profiles/edit_superuser.html'
    context = {
        'form': form,
        'user': user,
    }

    return render(request, template, context)


@login_required
def delete_superuser(request, user_id):
    """ Delete a superuser """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    # Don't allow deleting yourself
    if int(user_id) == request.user.id:
        messages.error(request, 'You cannot remove your own superuser status.')
        return redirect('product_management')

    user = get_object_or_404(User, id=user_id, is_superuser=True)

    # Revoke superuser status instead of deleting the account
    user.is_superuser = False
    user.is_staff = False
    user.save()

    messages.success(request, f'Superuser status removed from {user.username}')
    return redirect('product_management')


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            # Show success message with product ID for debugging
            messages.success(
                request,
                f'Successfully added product! (ID: {product.id})'
            )
            return redirect('product_management')
        else:
            # Show detailed form errors to help debug
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm()

    template = 'profiles/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Successfully updated product: {product.name}'
            )
            return redirect('product_management')
        else:
            # Show detailed form errors to help debug
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm(instance=product)

    template = 'profiles/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')

    return redirect('product_management')


@login_required
def add_category(request):
    """ Add a category """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added category!')
            return redirect('product_management')
        else:
            messages.error(
                request,
                'Failed to add category. Please ensure the form is valid.'
            )
    else:
        form = CategoryForm()

    template = 'profiles/add_category.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_category(request, category_id):
    """ Edit a category """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated category!')
            return redirect('product_management')
        else:
            messages.error(
                request,
                'Failed to update category. Please ensure the form is valid.'
            )
    else:
        form = CategoryForm(instance=category)

    template = 'profiles/edit_category.html'
    context = {
        'form': form,
        'category': category,
    }

    return render(request, template, context)


@login_required
def delete_category(request, category_id):
    """ Delete a category """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    messages.success(request, 'Category deleted!')

    return redirect('product_management')


@login_required
def product_management(request):
    """ Display the product management page """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect('profile')

    products = Product.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    superusers = User.objects.filter(
        is_superuser=True).order_by('username')

    template = 'profiles/product_management.html'
    context = {
        'products': products,
        'categories': categories,
        'superusers': superusers,
    }

    return render(request, template, context)
