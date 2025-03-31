from .models import Review
from rest_framework import serializers

class ReviewSerialzer(serializers.ModelSerializer):
    serializers.FloatField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = '__all__'