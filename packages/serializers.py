from rest_framework import serializers
from .models import Packages

class PackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = '__all__'
        
    def validate_price(self,value):
        if value < 0:
            raise serializers.ValidationError("Price must be positive.")
        return value  