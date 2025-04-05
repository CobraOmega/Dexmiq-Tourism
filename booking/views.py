from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Booking
from .serializers import BookingSerializer
from packages.models import Packages

class IsOwnerOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.is_staff:
            return True
        
        return obj.customer.user == request.user

#CREATE
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

#READ one booking
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

#DELETE/
class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

# Payment integration (from booking to payment)
@api_view(['GET', 'POST'])
def initiate_payment(request, pk):
    # Check if user is authenticated (via session or token)
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, 
                      status=status.HTTP_401_UNAUTHORIZED)
    
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check if user is authorized to pay for this booking
    if booking.customer.user != request.user and not request.user.is_staff:
        return Response({"error": "You are not authorized to make payment for this booking."},
                       status=status.HTTP_403_FORBIDDEN)
    
    # Check if booking is already paid or cancelled
    if booking.status == 'cancelled':
        return Response({"error": "Cannot process payment for a cancelled booking."},
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Return the checkout URL for API clients
    checkout_url = request.build_absolute_uri(f'/payment/checkout/{booking.id}/')
    return Response({
        "message": "Redirecting to payment gateway",
        "checkout_url": checkout_url,
        "booking_id": booking.id,
        "amount": booking.total_price
    })

# Separate view for web payment flow
@login_required
def web_initiate_payment(request, pk):
    
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check if user is authorized to pay for this booking
    if booking.customer.user != request.user and not request.user.is_staff:
        return render(request, "error.html", 
                     {"message": "You are not authorized to make payment for this booking."})
    
    # Check if booking is already paid or cancelled
    if booking.status == 'cancelled':
        return render(request, "error.html", 
                     {"message": "Cannot process payment for a cancelled booking."})
    
    # Direct redirect to payment checkout
    return redirect(f'/payment/checkout/{booking.id}/')

@login_required
def booking_view(request, package_id):
   
    package = get_object_or_404(Packages, id=package_id)
    min_date = timezone.now().date()
    
    # Check if user has a profile
    error_message = None
    try:
        request.user.customer_profile
    except AttributeError:
        error_message = "You need to complete your customer profile before booking. Please update your profile information."
    
    context = {
        'package': package,
        'min_date': min_date,
        'user': request.user
    }
    
    if error_message:
        context['error_message'] = error_message
    
    return render(request, 'booking.html', context)

@login_required
def create_booking(request):
    
    if request.method == 'POST':
        
        package_id = request.POST.get('package_id')
        travel_date = request.POST.get('travel_date')
        number_of_people = request.POST.get('number_of_people')
        
        
        package = get_object_or_404(Packages, id=package_id)
        
        try:
            
            try:
                customer = request.user.customer_profile
            except AttributeError:
                return render(request, 'booking.html', {
                    'package': package,
                    'min_date': timezone.now().date(),
                    'user': request.user,
                    'error_message': "You need to complete your customer profile before booking. Please update your profile information."
                })
            
            # Create the booking
            booking = Booking(
                package=package,
                customer=customer,
                travel_date=travel_date,
                number_of_people=number_of_people
            )
            
            booking.save()
            # Redirect to payment or confirmation
            return redirect(reverse('initiate_payment', args=[booking.id]))
        except Exception as e:
            # Handle validation errors
            return render(request, 'booking.html', {
                'package': package,
                'min_date': timezone.now().date(),
                'user': request.user,
                'error_message': str(e)
            })
    
    # If not POST, redirect to homepage
    return redirect('homepage')
