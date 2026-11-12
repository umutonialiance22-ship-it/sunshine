from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "room_number",
        "category",
        "price",
        "max_occupancy",
    )

    search_fields = (
        "room_number",
        "category",
    )

    list_filter = (
        "category",
    )