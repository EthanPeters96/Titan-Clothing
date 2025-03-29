from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import logging

from checkout.webhook_handler import StripeWH_Handler

import stripe

logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    try:
        # Setup
        wh_secret = settings.STRIPE_WH_SECRET
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Log the incoming request details
        logger.info("Received webhook request")
        logger.info(f"Request headers: {dict(request.META)}")
        logger.info(f"Request body: {request.body.decode('utf-8')}")

        # Verify webhook secret is set
        if not wh_secret:
            logger.error("STRIPE_WH_SECRET is not set")
            return HttpResponse(
                content="Webhook secret not configured",
                status=500
            )

        # get the webhook data and verify its signature
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        if not sig_header:
            logger.error("No Stripe signature header found")
            return HttpResponse(
                content="No Stripe signature header",
                status=400
            )

        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, wh_secret
            )
            logger.info(f"Webhook signature verified successfully for event type: {event['type']}")  # noqa: E501
        except ValueError as e:
            logger.error(f"Invalid payload: {str(e)}")
            return HttpResponse(
                content=f"Invalid payload: {str(e)}",
                status=400
            )
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {str(e)}")
            return HttpResponse(
                content=f"Invalid signature: {str(e)}",
                status=400
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return HttpResponse(
                content=f"Unexpected error: {str(e)}",
                status=400
            )

        # Set up a webhook handler
        handler = StripeWH_Handler(request)

        # Map webhook events to relevant handler functions
        event_map = {
            'payment_intent.succeeded': handler.handle_payment_intent_succeeded,  # noqa: E501
            'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,  # noqa: E501
        }

        # Get the webhook type from Stripe
        event_type = event['type']

        # If there's a handler for it, get it from the event map
        # Use the generic one by default
        event_handler = event_map.get(event_type, handler.handle_event)

        # Call the event handler with the event
        response = event_handler(event)
        return response

    except Exception as e:
        logger.error(f"Unhandled exception in webhook: {str(e)}")
        return HttpResponse(
            content=f"Unhandled exception: {str(e)}",
            status=500
        )
