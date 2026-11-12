from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reservation",
        "transaction_ref",
        "amount",
        "status",
        "created_at",
    )

    search_fields = (
        "transaction_ref",
        "reservation__guest__full_name",
        "reservation__guest__email",
    )

    list_filter = (
        "status",
        "created_at",
    )