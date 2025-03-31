from django.contrib import admin
from .models import Packages

@admin.register(Packages)
class PackagesAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'price', 
        'destination', 
        'duration', 
        'rating', 
        'is_active', 
        'created_at'
    ]
    list_filter = ['is_active', 'destination', 'duration']
    search_fields = ['title', 'destination', 'short_description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'image', 'price', 'duration', 'destination')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'long_description')
        }),
        ('Package Details', {
            'fields': ('highlights', 'itinerary', 'inclusions', 'exclusions')
        }),
        ('Statistics', {
            'fields': ('rating', 'reviews')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )