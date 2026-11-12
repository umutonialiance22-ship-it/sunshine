# payments/services.py

import uuid

from django.db import transaction

from .models import Payment
from reservations.models import Reservation


def generate_transaction_ref():
    """
    Generate a unique transaction reference.
    Example:
    SUN-8F3A91D2C4
    """
    return f"SUN-{uuid.uuid4().hex[:10].upper()}"


def calculate_reservation_amount(reservation):
    """
    Calculate the total amount for a reservation.

    Example:
    Room price = 100,000 RWF
    3 nights = 300,000 RWF
    """

    number_of_nights = (
        reservation.check_out_date - reservation.check_in_date
    ).days

    if number_of_nights <= 0:
        raise ValueError(
            "Check-out date must be after check-in date."
        )

    room_price = reservation.room.price

    total_amount = room_price * number_of_nights

    return total_amount


@transaction.atomic
def create_payment_for_reservation(reservation):
    """
    Create a Pending payment record for a reservation.

    KitovuPay integration will be added later when
    the API documentation is received.
    """

    if reservation.status != "Pending":
        raise ValueError(
            "Payment can only be created for a Pending reservation."
        )

    amount = calculate_reservation_amount(reservation)

    transaction_ref = generate_transaction_ref()

    payment = Payment.objects.create(
        reservation=reservation,
        transaction_ref=transaction_ref,
        amount=amount,
        status="Pending",
    )

    return payment