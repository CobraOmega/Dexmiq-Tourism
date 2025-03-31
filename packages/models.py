from django.db import models
from customer.models import Customer

class Packages(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = 'packages/')
    rating = models.FloatField(default = 0.0)
    reviews = models.IntegerField(default = 0)
    price = models.IntegerField(default = 0)
    duration = models.CharField(max_length = 50, default = 'Unknown')
    destination = models.CharField(max_length = 50, default=  'Unknown')
    short_description = models.TextField(default ="No short description available")
    long_description = models.TextField(default ="No long description available")
    highlights = models.TextField(default = "No highlights specified")
    itinerary = models.TextField(default = "No itinerary specified")
    inclusions = models.TextField(default = "No inclusions specified")
    exclusions = models.TextField(default = "No exclusions specified")
    customers = models.ManyToManyField(Customer, through='booking.Booking', related_name='packages')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']  # Packages by Last created

    def __str__(self):
        return self.title
    
    def is_visible(self):
        return self.is_active
    
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return None
