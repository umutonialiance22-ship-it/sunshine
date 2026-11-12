from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = [
            "id",
            "guest",
            "room",
            "check_in_date",
            "check_out_date",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "status",
            "created_at",
        ]