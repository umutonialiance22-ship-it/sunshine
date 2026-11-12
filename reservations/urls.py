from django.urls import path

from .views import (
    ReservationListCreateView,
    ReservationDetailView,
    ReservationCancelView,
)


urlpatterns = [

    path(
        "",
        ReservationListCreateView.as_view(),
        name="reservation-list-create"
    ),

    path(
        "<int:id>/",
        ReservationDetailView.as_view(),
        name="reservation-detail"
    ),

    path(
        "<int:pk>/cancel/",
        ReservationCancelView.as_view(),
        name="reservation-cancel"
    ),

]