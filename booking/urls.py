from django.urls import path
from .views import BookingCreateView, BookingDeleteView, BookingDetailView, BookingReadView, BookingUpdateView, initiate_payment

urlpatterns = [
    path('bookings/create/', BookingCreateView.as_view(), name = 'booking-create'), #create a booking
    path('bookings/', BookingReadView.as_view(), name = 'booking-list'), #read all bookings
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name = 'booking-detail'), #read one booking
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name = 'booking-update'), #update one booking
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name = 'booking-delete'), #delete one booking 
    path('bookings/<int:pk>/pay/', initiate_payment, name = 'booking-payment'), #initiate payment for a booking
]