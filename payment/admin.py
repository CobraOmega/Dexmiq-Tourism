from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_charge_id', 'amount', 'status', 'created_at')
    search_fields = ('user__username', 'stripe_charge_id')