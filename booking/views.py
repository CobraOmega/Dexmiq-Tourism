from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.urls import reverse
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
        queryset = Booking.objects.all()
        
        # Admin users can see all bookings, users can only see their own
        if not self.request.user.is_staff:
            queryset = queryset.filter(customer__user=self.request.user)
        
        # Filter by status (pending, confirmed, cancelled)
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by booking date
        booking_date = self.request.query_params.get('booking_date', None)
        if booking_date:
            queryset = queryset.filter(booking_date=booking_date)
        
        # Filter by travel date
        travel_date = self.request.query_params.get('travel_date', None)
        if travel_date:
            queryset = queryset.filter(travel_date=travel_date)
        
        # Filter by package
        package_id = self.request.query_params.get('package_id', None)
        if package_id:
            queryset = queryset.filter(package_id=package_id)
            
        # Sort results
        ordering = self.request.query_params.get('ordering', '-booking_date')  # Default: newest first
        return queryset.order_by(ordering)

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

# Payment integration (from booking to payment)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request, pk):
    """
    Initiate payment for a booking.
    This endpoint validates the booking and returns the payment checkout URL.
    """
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check if user is authorized to pay for this booking
    if not request.user.is_staff and booking.customer.user != request.user:
        return Response(
            {"error": "You are not authorized to make payment for this booking."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Check if booking is already paid or cancelled
    if booking.status == 'cancelled':
        return Response(
            {"error": "Cannot process payment for a cancelled booking."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Generate checkout URL
    checkout_url = request.build_absolute_uri(reverse('checkout', args=[booking.id]))
    
    return Response({
        "message": "Redirecting to payment gateway",
        "checkout_url": checkout_url,
        "booking_id": booking.id,
        "amount": booking.total_price
    })
