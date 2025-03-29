from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        try:
            intent = event.data.object
            pid = intent.id

            # Use .get() to prevent missing key errors
            bag = intent.metadata.get("bag", "{}")
            save_info = intent.metadata.get("save_info", False)

            # Get the billing and shipping details with proper null checks
            billing_details = intent.billing_details if hasattr(intent, 'billing_details') else {}  # noqa: E501
            shipping_details = intent.shipping if hasattr(intent, 'shipping') else {}  # noqa: E501

            # Ensure shipping_details.address exists before modifying it
            if shipping_details and shipping_details.get("address"):
                for field, value in shipping_details["address"].items():
                    if value == "":
                        shipping_details["address"][field] = None

            # Prevent division errors if intent.amount is missing
            grand_total = round((intent.amount or 0) / 100, 2)

            # Update profile information if save_info was checked
            profile = None
            username = intent.metadata.get('username', 'AnonymousUser')
            if username != 'AnonymousUser':
                try:
                    profile = UserProfile.objects.get(user__username=username)
                    if save_info and shipping_details:
                        profile.default_phone_number = shipping_details.get('phone')  # noqa: E501
                        profile.default_country = shipping_details.get('address', {}).get('country')  # noqa: E501
                        profile.default_postcode = shipping_details.get('address', {}).get('postal_code')  # noqa: E501
                        profile.default_town_or_city = shipping_details.get('address', {}).get('city')  # noqa: E501
                        profile.default_street_address1 = shipping_details.get('address', {}).get('line1')  # noqa: E501
                        profile.default_street_address2 = shipping_details.get('address', {}).get('line2')  # noqa: E501
                        profile.default_county = shipping_details.get('address', {}).get('state')  # noqa: E501
                        profile.save()
                except UserProfile.DoesNotExist:
                    profile = None

            order_exists = False
            attempt = 1
            while attempt <= 5:
                try:
                    order = Order.objects.get(
                        full_name__iexact=shipping_details.get('name', ''),
                        email__iexact=billing_details.get('email', ''),
                        phone_number__iexact=shipping_details.get('phone', ''),
                        country__iexact=shipping_details.get('address', {}).get('country', ''),  # noqa: E501
                        postcode__iexact=shipping_details.get('address', {}).get('postal_code', ''),  # noqa: E501
                        town_or_city__iexact=shipping_details.get('address', {}).get('city', ''),  # noqa: E501
                        street_address1__iexact=shipping_details.get('address', {}).get('line1', ''),  # noqa: E501
                        street_address2__iexact=shipping_details.get('address', {}).get('line2', ''),  # noqa: E501
                        county__iexact=shipping_details.get('address', {}).get('state', ''),  # noqa: E501
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    order_exists = True
                    break
                except Order.DoesNotExist:
                    attempt += 1
                    time.sleep(1)

            if order_exists:
                self._send_confirmation_email(order)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',  # noqa: E501
                    status=200)
            else:
                order = None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.get('name', ''),
                        user_profile=profile,
                        email=billing_details.get('email', ''),
                        phone_number=shipping_details.get('phone', ''),
                        country=shipping_details.get('address', {}).get('country', ''),  # noqa: E501
                        postcode=shipping_details.get('address', {}).get('postal_code', ''),  # noqa: E501
                        town_or_city=shipping_details.get('address', {}).get('city', ''),  # noqa: E501
                        street_address1=shipping_details.get('address', {}).get('line1', ''),  # noqa: E501
                        street_address2=shipping_details.get('address', {}).get('line2', ''),  # noqa: E501
                        county=shipping_details.get('address', {}).get('state', ''),  # noqa: E501
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    for item_id, item_data in json.loads(bag).items():
                        product = Product.objects.get(id=item_id)
                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                            order_line_item.save()
                        else:
                            for size, quantity in item_data['items_by_size'].items():  # noqa: E501
                                order_line_item = OrderLineItem(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    product_size=size,
                                )
                                order_line_item.save()
                except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {str(e)}',  # noqa: E501
                        status=500)

                self._send_confirmation_email(order)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',  # noqa: E501
                    status=200)
        except Exception as e:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {str(e)}',
                status=500)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
