from rest_framework import viewsets
from .models import Review
from .serializer import ReviewSerialzer
#from rest_framework.permissions import IsAuthenticated (after authorisation enable)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerialzer
    #permission_classes = [IsAuthenticated] (after authorisation enable)