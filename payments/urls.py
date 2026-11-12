from django.urls import path

from .views import (
    PaymentInitializeView,
    PaymentConfirmTestView,
    PaymentWebhookView,
)


urlpatterns = [
    path(
        "initialize/",
        PaymentInitializeView.as_view(),
        name="payment-initialize",
    ),

    path(
        "confirm-test/<int:payment_id>/",
        PaymentConfirmTestView.as_view(),
        name="payment-confirm-test",
    ),

    path(
        "webhook/",
        PaymentWebhookView.as_view(),
        name="payment-webhook",
    ),
]