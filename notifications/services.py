from django.conf import settings
from django.core.mail import send_mail


def send_front_desk_notification(reservation, payment):

    guest = reservation.guest
    room = reservation.room

    subject = (
        f"Sunshine Hotel - Confirmed Booking - "
        f"Room {room.room_number}"
    )

    message = f"""
A new hotel reservation has been successfully paid and confirmed.

GUEST DETAILS
-------------
Name: {guest.full_name}
Email: {guest.email}
Phone: {guest.phone}

ROOM DETAILS
------------
Room Number: {room.room_number}
Category: {room.category}

STAY DETAILS
------------
Check-in: {reservation.check_in_date}
Check-out: {reservation.check_out_date}

PAYMENT DETAILS
---------------
Amount: {payment.amount} RWF
Transaction Reference: {payment.transaction_ref}
Payment Status: {payment.status}

Please manually record this reservation in the
Smart Biashara HMS.

This is an automated notification from Sunshine Hotel's
booking platform.
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            settings.FRONT_DESK_EMAIL
        ],
        fail_silently=False,
    )

    return True