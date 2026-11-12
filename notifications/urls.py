from django.urls import path

from .views import TestFrontDeskNotificationView


urlpatterns = [

    path(
        "test/<int:reservation_id>/",
        TestFrontDeskNotificationView.as_view(),
        name="test-front-desk-notification"
    ),

]