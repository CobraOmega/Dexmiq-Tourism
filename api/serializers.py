from rest_framework import serializers
from customer.models import Customer  #Importing Customer model

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'  #Serializes all fields for customer