from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Customusermanager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email must be filled!")
        
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email) #sets email as username by default
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):  #Inherits Django's User model
    email = models.EmailField(unique=True)  #For login
    phone_number = models.CharField(max_length=15, unique = True)
    country = models.CharField(max_length=50)
    

    USERNAME_FIELD = 'email'  #Use email as login instead of username
    REQUIRED_FIELDS = []  #For username field

    objects = Customusermanager()

    class Meta:
        app_label = 'customer'

    def __str__(self):
        return self.email
    
    # Auto-create a Customer when a user is created
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  #Save CustomUser (user) first
        Customer.objects.get_or_create(user=self)  # Create a customer if not exists

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name="customer_profile")  #User ID will be Customer ID
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return self.user.email
    
