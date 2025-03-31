import uuid
from booking.models import Booking
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Payment(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    payment_id = models.UUIDField(default=uuid.uuid4, unique = True, editable = False)  #Unique ID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE) #Track payment for specific booking
    stripe_charge_id = models.CharField(max_length = 100, unique = True, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length = 20, choices = status_choices, default = 'pending')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.amount} - {self.status}", 