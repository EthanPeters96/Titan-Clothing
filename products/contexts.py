from products.models import Category


def categories_processor(request):
    """
    Context processor to provide category data for the navigation menu
    """
    # Get all categories and ensure friendly names are available
    all_categories = Category.objects.all()

    # Prepare category data
    for category in all_categories:
        has_method = hasattr(category, 'get_friendly_name')
        if not category.friendly_name and has_method:
            category.friendly_name = category.get_friendly_name()

    # Check if the Category model has a 'group' field
    has_group_field = hasattr(Category, 'group')

    if has_group_field:
        # If the model has been updated with a group field, use it for grouping
        # Get unique groups
        groups = Category.objects.exclude(group__isnull=True).exclude(
            group__exact='').values_list('group', flat=True).distinct()

        # Create a dictionary of category groups
        category_groups = {}
        for group in groups:
            group_categories = all_categories.filter(group=group)
            category_groups[group] = group_categories

        # Create context with dynamic grouping
        context = {
            'all_categories': all_categories,
            'category_groups': category_groups,
            'has_category_groups': True,
        }
    else:
        # Fall back to manual grouping if the model hasn't been updated yet
        clothing_categories = all_categories.filter(
            name__in=['hoodies', 't-shirts', 'jumpers'])
        accessories_categories = all_categories.filter(
            name__in=['bags', 'shoes'])

        # Create context with manual grouping
        context = {
            'all_categories': all_categories,
            'clothing_categories': clothing_categories,
            'accessories_categories': accessories_categories,
            'has_category_groups': False,
        }

    return context
