import uuid

from django.db import transaction

from .models import Payment


def generate_transaction_ref():
    return f"SUN-{uuid.uuid4().hex[:10].upper()}"


def calculate_reservation_amount(reservation):
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


@transaction.atomic
def confirm_payment(payment):
    """
    Confirm a payment and its reservation atomically.

    If anything fails inside this transaction,
    neither the payment nor reservation will be changed.
    """

    payment = (
        Payment.objects
        .select_for_update()
        .select_related("reservation")
        .get(id=payment.id)
    )

    reservation = (
        payment.reservation
    )

    if payment.status == "Success":
        return payment, reservation, False

    if payment.status == "Failed":
        raise ValueError(
            "A failed payment cannot be confirmed."
        )

    if reservation.status != "Pending":
        raise ValueError(
            "Only Pending reservations can be confirmed."
        )

    payment.status = "Success"
    payment.save(update_fields=["status"])

    reservation.status = "Confirmed"
    reservation.save(update_fields=["status"])

    return payment, reservation, True