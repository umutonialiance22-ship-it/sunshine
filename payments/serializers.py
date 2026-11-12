from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id",
            "reservation",
            "transaction_ref",
            "amount",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "transaction_ref",
            "status",
            "created_at",
        ]