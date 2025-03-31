from django.urls import path
from .views import BookingCreateView, BookingDeleteView, BookingDetailView, BookingReadView

urlpatterns = [
    path('bookings/create/', BookingCreateView.as_view(), name = 'booking-create'), #create a booking
    path('bookings/', BookingReadView.as_view(), name = 'booking-list'), #read all bookings
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name = 'booking-detail'), #read one booking
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name = 'booking-delete'), #delete one booking 
]