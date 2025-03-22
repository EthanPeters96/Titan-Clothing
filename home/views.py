from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def index(request):
    """ A view to display the index page """
    try:
        # Return a simple view with no product references
        return render(request, 'home/index.html')
    except Exception as e:
        messages.error(request, f"Error loading homepage: {str(e)}")
        return redirect(reverse('products'))


def faq(request):
    """ A view to display the FAQ page """

    return render(request, 'home/faq.html')


def returns(request):
    """ A view to display the returns policy page """

    return render(request, 'home/returns.html')


def contact(request):
    """ A view to display and handle the contact page """

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('firstName', '')
        last_name = request.POST.get('lastName', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        order_number = request.POST.get('orderNumber', '')
        subject_type = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # Basic validation
        if not (first_name and last_name and email and subject_type and message):  # noqa
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'home/contact.html')

        # Create full subject
        subject_map = {
            'order': 'Order Status Inquiry',
            'return': 'Returns & Exchanges Question',
            'product': 'Product Information Request',
            'account': 'Account Help',
            'feedback': 'Customer Feedback',
            'other': 'General Inquiry',
        }

        full_subject = subject_map.get(subject_type, 'Website Contact Form')

        # Create email body
        email_body = f"""
        Name: {first_name} {last_name}
        Email: {email}
        Phone: {phone}
        Order Number: {order_number}
        Subject: {full_subject}

        Message:
        {message}
        """

        # Try to send email
        try:
            # Send email to shop owner
            send_mail(
                f'Titan Clothing Contact Form: {full_subject}',
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            # Send confirmation email to customer
            customer_subject = 'Thank you for contacting Titan Clothing'
            customer_body = f"""
            Dear {first_name},

            Thank you for contacting Titan Clothing.
            We have received your message and will get back to you within
            1-2 business days.

            Your message details:
            Subject: {full_subject}

            Best regards,
            The Titan Clothing Team
            """

            send_mail(
                customer_subject,
                customer_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request,
                             'Your message has been sent successfully. '
                             'We will get back to you soon!')
            return render(request, 'home/contact.html')

        except Exception:
            messages.error(request,
                           'Sorry, there was an error sending your message. '
                           'Please try again later or email us directly at '
                           'support@titanclothing.com')

    return render(request, 'home/contact.html')
