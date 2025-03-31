from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from customer.models import Customer
from packages.models import Packages

class Review(models.Model):
    package = models.ForeignKey('packages.Packages', on_delete=models.CASCADE, null=True, blank=True) #nullable
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, null=True, blank=True) #reviewer ,nullable
    review = models.TextField() #Review text
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)]) #Rating: 1-5

    def __str__ (self):
        return f"{self.review} - {self.rating} star"