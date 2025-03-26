import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.core import mail
from django.contrib.messages import get_messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from .views import index, faq, returns, contact


@pytest.mark.django_db
class TestHomeViews:
    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    @pytest.fixture
    def request_with_session(self, request_factory):
        request = request_factory.get('/')
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        message_middleware = MessageMiddleware(request)
        message_middleware.process_request(request)
        return request

    def test_index_view(self, request_with_session):
        response = index(request_with_session)
        assert response.status_code == 200
        assert 'home/index.html' in [t.name for t in response.templates]

    def test_faq_view(self, request_with_session):
        response = faq(request_with_session)
        assert response.status_code == 200
        assert 'home/faq.html' in [t.name for t in response.templates]

    def test_returns_view(self, request_with_session):
        response = returns(request_with_session)
        assert response.status_code == 200
        assert 'home/returns.html' in [t.name for t in response.templates]

    def test_contact_view_get(self, request_with_session):
        response = contact(request_with_session)
        assert response.status_code == 200
        assert 'home/contact.html' in [t.name for t in response.templates]

    def test_contact_view_post_success(self, request_with_session, settings):
        # Configure test email settings
        settings.DEFAULT_FROM_EMAIL = 'test@example.com'
        settings.EMAIL_BACKEND = (
            'django.core.mail.backends.locmem.EmailBackend'
        )

        request = request_with_session
        request.method = 'POST'
        request.POST = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'orderNumber': 'ORDER123',
            'subject': 'order',
            'message': 'Test message'
        }
        response = contact(request)
        assert response.status_code == 200
        assert 'home/contact.html' in [t.name for t in response.templates]

        # Check success message
        messages = list(get_messages(request))
        assert len(messages) == 1
        assert str(messages[0]) == (
            'Your message has been sent successfully. '
            'We will get back to you soon!'
        )

        # Check emails
        assert len(mail.outbox) == 2
        # Check admin email
        assert mail.outbox[0].subject == (
            'Titan Clothing Contact Form: Order Status Inquiry'
        )
        assert mail.outbox[0].from_email == 'test@example.com'
        assert mail.outbox[0].to == ['test@example.com']
        assert 'Name: John Doe' in mail.outbox[0].body
        assert 'Email: john@example.com' in mail.outbox[0].body
        assert 'Phone: 1234567890' in mail.outbox[0].body
        assert 'Order Number: ORDER123' in mail.outbox[0].body
        assert 'Message:\nTest message' in mail.outbox[0].body

        # Check customer email
        assert mail.outbox[1].subject == (
            'Thank you for contacting Titan Clothing'
        )
        assert mail.outbox[1].from_email == 'test@example.com'
        assert mail.outbox[1].to == ['john@example.com']
        assert 'Dear John,' in mail.outbox[1].body
        assert 'Subject: Order Status Inquiry' in mail.outbox[1].body

    def test_contact_view_post_missing_fields(self, request_with_session):
        request = request_with_session
        request.method = 'POST'
        request.POST = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'subject': 'order',
            'message': ''  # Missing required field
        }
        response = contact(request)
        assert response.status_code == 200
        assert 'home/contact.html' in [t.name for t in response.templates]

        # Check error message
        messages = list(get_messages(request))
        assert len(messages) == 1
        assert str(messages[0]) == 'Please fill in all required fields.'

    def test_contact_view_post_email_error(self, request_with_session, settings):
        # Configure test email settings to raise an error
        settings.DEFAULT_FROM_EMAIL = 'test@example.com'
        settings.EMAIL_BACKEND = (
            'django.core.mail.backends.dummy.EmailBackend'
        )

        request = request_with_session
        request.method = 'POST'
        request.POST = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'orderNumber': 'ORDER123',
            'subject': 'order',
            'message': 'Test message'
        }
        response = contact(request)
        assert response.status_code == 200
        assert 'home/contact.html' in [t.name for t in response.templates]

        # Check error message
        messages = list(get_messages(request))
        assert len(messages) == 1
        assert str(messages[0]) == (
            'Sorry, there was an error sending your message. '
            'Please try again later or email us directly at '
            'support@titanclothing.com'
        )
