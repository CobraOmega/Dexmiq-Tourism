from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a booking or admins to view/edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users can access any booking
        if request.user.is_staff:
            return True
        # Otherwise, users can only access their own bookings
        return obj.customer.user == request.user

#CREATE
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

#READ/RETRIEVE one booking
class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

#READ All bookings
class BookingReadView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Admin users can see all bookings
        if self.request.user.is_staff:
            return Booking.objects.all()
        # Regular users can only see their own bookings
        return Booking.objects.filter(customer__user=self.request.user)

#UPDATE
class BookingUpdateView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

#DELETE/DESTROY
class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
