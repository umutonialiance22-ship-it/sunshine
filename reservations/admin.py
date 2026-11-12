from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "guest",
        "room",
        "check_in_date",
        "check_out_date",
        "status",
        "created_at",
    )

    search_fields = (
        "guest__full_name",
        "guest__email",
        "room__room_number",
    )

    list_filter = (
        "status",
        "check_in_date",
        "check_out_date",
    )