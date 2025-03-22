from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    try:
        for item_id, item_data in bag.items():
            try:
                product = get_object_or_404(Product, pk=item_id)

                if isinstance(item_data, int):
                    total += item_data * product.price
                    product_count += item_data
                    bag_items.append({
                        'item_id': item_id,
                        'quantity': item_data,
                        'product': product,
                    })
                else:
                    for size, quantity in item_data['items_by_size'].items():
                        total += quantity * product.price
                        product_count += quantity
                        bag_items.append({
                            'item_id': item_id,
                            'quantity': quantity,
                            'product': product,
                            'size': size,
                        })
            except Exception:
                # If a product cannot be found, just skip it
                continue

        if total < settings.FREE_DELIVERY_THRESHOLD:
            delivery_percentage = settings.STANDARD_DELIVERY_PERCENTAGE / 100
            delivery = total * Decimal(delivery_percentage)
            free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
        else:
            delivery = 0
            free_delivery_delta = 0

        grand_total = total + delivery

    except Exception:
        # If anything goes wrong, provide empty values
        bag_items = []
        total = 0
        product_count = 0
        delivery = 0
        free_delivery_delta = 0
        grand_total = 0

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    return context
