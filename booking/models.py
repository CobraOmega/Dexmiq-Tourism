from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from customer.models import Customer
from packages.models import Packages

class Booking(models.Model):
    id = models.AutoField(primary_key = True)
    package = models.ForeignKey('packages.Packages', on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey("customer.Customer", on_delete = models.CASCADE, related_name='bookings')
    booking_date = models.DateField(auto_now_add = True)
    travel_date = models.DateField()
    number_of_people = models.IntegerField(default = 1)
    total_price = models.FloatField(editable = False)
    status = models.CharField(
        max_length = 20,
        choices = [
            ('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default = "pending"
    )

    # Calculation of price according to number of people
    def save(self, *args, **kwargs):
        if self.package:
            self.total_price = self.package.price * self.number_of_people

    # Prevention of double booking
        existing_booking = Booking.objects.filter(
            customer = self.customer,
            package = self.package,
            travel_date = self.travel_date
        ).exclude(id=self.id)
    
        if existing_booking.exists():
            raise ValidationError("You have already booking for selected date!")
        
        super().save(*args, **kwargs)

    # Validation of booking (number of people, date of travel)
    def clean(self):
        if self.travel_date < now().date():
            raise ValidationError("Travel Date Cannot be in Past!")
        
        if self.number_of_people <=0:
            raise ValidationError("Minimum of 1 people required for booking!")

    def __str__(self):
        return f"Booking {self.id} - {self.customer.user.first_name} {self.customer.user.last_name} - {self.package.title}"