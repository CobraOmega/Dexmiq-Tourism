from django.urls import path, include

urlpatterns = [
    path('', include('customer.urls')), #For Customer API, can be accessed by /api/customer/
    path('', include('review.urls')),   #For Review API, can be accessed by /api/review/
    path('', include('packages.urls')), #For Packages API, can be accessed by /api/packages/
    path('', include('booking.urls')), #For Booking API, can be accessed by /api/booking/
]