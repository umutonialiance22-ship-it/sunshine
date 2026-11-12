from datetime import date

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer
from reservations.models import Reservation


class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class AvailableRoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        check_in = request.query_params.get("check_in")
        check_out = request.query_params.get("check_out")

        # Check that both dates were provided
        if not check_in or not check_out:
            return Response(
                {"error": "check_in and check_out are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convert strings into date objects
        try:
            check_in_date = date.fromisoformat(check_in)
            check_out_date = date.fromisoformat(check_out)
        except ValueError:
            return Response(
                {"error": "Dates must use YYYY-MM-DD format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check that checkout is after checkin
        if check_in_date >= check_out_date:
            return Response(
                {"error": "Check-out must be after check-in."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find rooms that already have overlapping reservations
        booked_room_ids = Reservation.objects.filter(
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date,
            status__in=["Pending", "Confirmed"]
        ).values_list(
            "room_id",
            flat=True
        )

        # Get rooms that are NOT booked
        available_rooms = Room.objects.exclude(
            id__in=booked_room_ids
        )

        serializer = self.get_serializer(
            available_rooms,
            many=True
        )

        return Response(serializer.data)

class RoomPriceCheckView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, *args, **kwargs):
        room_id = request.query_params.get("room_id")

        if not room_id:
            return Response(
                {"error": "room_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {"error": "Room not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "room_id": room.id,
                "room_number": room.room_number,
                "current_price": room.price,
                "currency": "RWF"
            },
            status=status.HTTP_200_OK
        )