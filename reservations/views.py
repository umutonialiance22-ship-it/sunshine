from datetime import date

from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Reservation
from .serializers import ReservationSerializer


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        guest = request.data.get("guest")
        room = request.data.get("room")
        check_in = request.data.get("check_in_date")
        check_out = request.data.get("check_out_date")

        # Check required fields
        if not guest or not room or not check_in or not check_out:
            return Response(
                {
                    "error": "guest, room, check_in_date and check_out_date are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convert dates
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

        # Check date order
        if check_in_date >= check_out_date:
            return Response(
                {
                    "error": "Check-out date must be after check-in date."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if room is already booked
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

        # Create reservation as Pending
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