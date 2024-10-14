from rest_framework import serializers
from core.models import Hotel

class HotelSerializers(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = '__all__'