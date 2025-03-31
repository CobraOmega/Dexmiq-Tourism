from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer

#CREATE
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

#READ/RETRIEVE one booking
class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

#READ All bookings
class BookingReadView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

#DELETE/DESTROY
class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
