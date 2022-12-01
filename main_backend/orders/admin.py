from django.contrib import admin
from orders.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display_links = (
        "created_by",
        "payment_token",
    )
    list_display = (
        "payment_token",
        "created_by",
        "phone",
        "created_at",
        "paid",
        "cash_on_delivery",
        "delivered",
    )


admin.site.register(Order, OrderAdmin)
