from django.urls import path

from .views import (
    RoomListView,
    AvailableRoomListView,
    RoomPriceCheckView,
)


urlpatterns = [
    path(
        "",
        RoomListView.as_view(),
        name="room-list"
    ),

    path(
        "available/",
        AvailableRoomListView.as_view(),
        name="available-rooms"
    ),

    path(
        "price/",
        RoomPriceCheckView.as_view(),
        name="room-price"
    ),
]