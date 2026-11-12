from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from reservations.models import Reservation
from payments.models import Payment

from .services import send_front_desk_notification


class TestFrontDeskNotificationView(APIView):

    def post(self, request, reservation_id):

        try:
            reservation = Reservation.objects.select_related(
                "guest",
                "room"
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

        try:
            payment = Payment.objects.get(
                reservation=reservation
            )

        except Payment.DoesNotExist:
            return Response(
                {
                    "error": "Payment not found for this reservation."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        try:

            send_front_desk_notification(
                reservation,
                payment
            )

        except Exception as error:

            return Response(
                {
                    "error": "Failed to send notification.",
                    "details": str(error)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "message": "Front desk notification sent successfully."
            },
            status=status.HTTP_200_OK
        )