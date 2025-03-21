from django.http import HttpResponse
from profiles.models import UserProfile
from .models import Order, OrderLineItem
from products.models import Product
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

import json
import time
import stripe


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
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
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info  # noqa

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details  # noqa
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Helper to get email safely (from billing_details)
        customer_email = None
        if hasattr(billing_details, 'email'):
            customer_email = billing_details.email

        # Helper to get name safely (from shipping_details or billing_details)
        customer_name = None
        if hasattr(shipping_details, 'name'):
            customer_name = shipping_details.name
        elif hasattr(billing_details, 'name'):
            customer_name = billing_details.name

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone

                # Handle all address fields with proper fallbacks
                # Country field
                if hasattr(shipping_details, 'country'):
                    profile.default_country = shipping_details.country
                elif (hasattr(shipping_details, 'address') and 
                      hasattr(shipping_details.address, 'country')):
                    profile.default_country = shipping_details.address.country

                # Postal code field
                if hasattr(shipping_details, 'postal_code'):
                    profile.default_postcode = shipping_details.postal_code
                elif (hasattr(shipping_details, 'address') and 
                      hasattr(shipping_details.address, 'postal_code')):
                    profile.default_postcode = shipping_details.address.postal_code  # noqa

                # City field
                if hasattr(shipping_details, 'city'):
                    profile.default_town_or_city = shipping_details.city
                elif (hasattr(shipping_details, 'address') and 
                      hasattr(shipping_details.address, 'city')):
                    profile.default_town_or_city = shipping_details.address.city  # noqa

                # Street address 1 field
                if hasattr(shipping_details, 'line1'):
                    profile.default_street_address1 = shipping_details.line1
                elif (hasattr(shipping_details, 'address') and 
                      hasattr(shipping_details.address, 'line1')):
                    profile.default_street_address1 = shipping_details.address.line1  # noqa

                # Street address 2 field
                if hasattr(shipping_details, 'line2'):
                    profile.default_street_address2 = shipping_details.line2
                elif (hasattr(shipping_details, 'address') and 
                      hasattr(shipping_details.address, 'line2')):
                    profile.default_street_address2 = shipping_details.address.line2  # noqa

                # County/state field
                if hasattr(shipping_details, 'state'):
                    profile.default_county = shipping_details.state
                elif (hasattr(shipping_details, 'address') and 
                      hasattr(shipping_details.address, 'state')):
                    profile.default_county = shipping_details.address.state

                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=customer_name,
                    email__iexact=customer_email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=self._get_address_field(
                        shipping_details, 'country'),
                    postcode__iexact=self._get_address_field(
                        shipping_details, 'postal_code'),
                    town_or_city__iexact=self._get_address_field(
                        shipping_details, 'city'),
                    street_address1__iexact=self._get_address_field(
                        shipping_details, 'line1'),
                    street_address2__iexact=self._get_address_field(
                        shipping_details, 'line2'),
                    county__iexact=self._get_address_field(
                        shipping_details, 'state'),
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
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',  # noqa
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=customer_name,
                    user_profile=profile,
                    email=customer_email,
                    phone_number=shipping_details.phone,
                    country=self._get_address_field(
                        shipping_details, 'country'),
                    postcode=self._get_address_field(
                        shipping_details, 'postal_code'),
                    town_or_city=self._get_address_field(
                        shipping_details, 'city'),
                    street_address1=self._get_address_field(
                        shipping_details, 'line1'),
                    street_address2=self._get_address_field(
                        shipping_details, 'line2'),
                    county=self._get_address_field(
                        shipping_details, 'state'),
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
                        for size, quantity in (
                                item_data['items_by_size'].items()):
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
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',  # noqa
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def _get_address_field(self, shipping_details, field_name):
        """
        Helper method to get address fields from shipping details,
        handling both direct access and access through the address object
        """
        if hasattr(shipping_details, field_name):
            return getattr(shipping_details, field_name)
        elif (hasattr(shipping_details, 'address') and 
              hasattr(shipping_details.address, field_name)):
            return getattr(shipping_details.address, field_name)
        return None
