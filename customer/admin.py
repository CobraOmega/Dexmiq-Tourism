from django.contrib import admin
from .models import Customer, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active',)
    ordering = ('email',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'full_name', 'phone_number', 'country', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('country', 'created_at')
    ordering = ('user__email',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'