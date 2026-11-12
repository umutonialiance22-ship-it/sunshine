# payments/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from reservations.models import Reservation

from .serializers import PaymentSerializer
from .services import create_payment_for_reservation


class PaymentInitializeView(APIView):
    """
    Initialize payment for a reservation.

    KitovuPay API integration will be added here
    after we receive the official API documentation.
    """

    def post(self, request):
        reservation_id = request.data.get("reservation_id")

        if not reservation_id:
            return Response(
                {
                    "error": "reservation_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reservation = Reservation.objects.select_related(
                "room",
                "guest"
            ).get(
                id=reservation_id
            )

        except Reservation.DoesNotExist:
            return Response(
                {
                    "error": "Reservation not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if reservation.status != "Pending":
            return Response(
                {
                    "error": "Payment can only be initialized for a Pending reservation."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent creating another payment
        # if this reservation already has one.
        if hasattr(reservation, "payment"):
            return Response(
                {
                    "error": "Payment has already been initialized for this reservation.",
                    "transaction_ref": reservation.payment.transaction_ref
                },
                status=status.HTTP_409_CONFLICT
            )

        try:
            payment = create_payment_for_reservation(
                reservation
            )

        except ValueError as error:
            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PaymentSerializer(payment)

        return Response(
            {
                "message": "Payment initialized successfully.",
                "payment": serializer.data,
                "next_step": "KitovuPay integration will be connected here."
            },
            status=status.HTTP_201_CREATED
        )


class PaymentWebhookView(APIView):
    """
    Payment gateway webhook.

    IMPORTANT:
    We are NOT implementing the real webhook verification yet.

    We need the official KitovuPay documentation first because
    the exact signature, headers and payload must come from
    their API specification.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        return Response(
            {
                "message": "Webhook endpoint is ready.",
                "status": "waiting_for_kitovupay_configuration"
            },
            status=status.HTTP_200_OK
        )