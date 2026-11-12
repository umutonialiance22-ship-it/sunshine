from datetime import date

from django.db import transaction
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Reservation
from .serializers import ReservationSerializer


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.select_related(
        "guest",
        "room"
    ).all()

    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):

        guest = request.data.get("guest")
        room = request.data.get("room")
        check_in = request.data.get("check_in_date")
        check_out = request.data.get("check_out_date")

        if not guest or not room or not check_in or not check_out:
            return Response(
                {
                    "error": "guest, room, check_in_date and check_out_date are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            check_in_date = date.fromisoformat(check_in)
            check_out_date = date.fromisoformat(check_out)

        except ValueError:
            return Response(
                {
                    "error": "Dates must use YYYY-MM-DD format."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if check_in_date >= check_out_date:
            return Response(
                {
                    "error": "Check-out date must be after check-in date."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if check_in_date < date.today():
            return Response(
                {
                    "error": "Check-in date cannot be in the past."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        overlapping_reservation = Reservation.objects.filter(
            room_id=room,
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date,
            status__in=["Pending", "Confirmed"]
        ).exists()

        if overlapping_reservation:
            return Response(
                {
                    "error": "This room is not available for the selected dates."
                },
                status=status.HTTP_409_CONFLICT
            )

        with transaction.atomic():

            reservation = Reservation.objects.create(
                guest_id=guest,
                room_id=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                status="Pending"
            )

        serializer = self.get_serializer(reservation)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class ReservationDetailView(generics.RetrieveAPIView):
    queryset = Reservation.objects.select_related(
        "guest",
        "room"
    ).all()

    serializer_class = ReservationSerializer

    lookup_field = "id"


class ReservationCancelView(APIView):
    def post(self, request, pk):

        try:
            reservation = Reservation.objects.get(pk=pk)

        except Reservation.DoesNotExist:
            return Response(
                {
                    "error": "Reservation not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if reservation.status == "Cancelled":
            return Response(
                {
                    "error": "Reservation is already cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if reservation.status == "Confirmed":
            return Response(
                {
                    "error": "Confirmed reservations cannot be cancelled through this endpoint."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.status = "Cancelled"
        reservation.save(update_fields=["status"])

        return Response(
            {
                "message": "Reservation cancelled successfully.",
                "reservation_id": reservation.id,
                "status": reservation.status
            },
            status=status.HTTP_200_OK
        )