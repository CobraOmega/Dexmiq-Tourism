from django.urls import path
from .views import (
    BookingCreateView, BookingDeleteView, BookingDetailView, 
    BookingReadView, BookingUpdateView, initiate_payment, web_initiate_payment,
    booking_view, create_booking
)

urlpatterns = [
    #API endpoints
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/', BookingReadView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking-delete'),
    path('bookings/<int:pk>/pay/', initiate_payment, name='booking-pay-api'),
    
    #Web views
    path('book/<int:package_id>/', booking_view, name='booking_view'),
    path('book/create/', create_booking, name='create_booking'),
    path('book/<int:pk>/pay/', web_initiate_payment, name='initiate_payment'),  # Web-specific URL for payment
]