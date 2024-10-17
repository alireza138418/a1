from rest_framework import serializers
from core.models import Hotel, Room

class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'room_number', 'price', 'type')

class HotelSerializers(serializers.ModelSerializer):

    rooms = RoomSerializers(many=True)
    class Meta:
        model = Hotel
        fields = '__all__'

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms' , None)
        hotel = Hotel.objects.create(**validated_data)
        for room_data in rooms_data:
            Room.objects.create(hotel=hotel, **room_data)

        return hotel

    def update(self, instance, validated_data):
        rooms_date = validated_data.pop('rooms')
        hotel = super.update(instance, validated_data)
        for room_date in rooms_date:
            room_instance = Room.objects.get(id=room_date['id'])
            room_instance.update(**room_date)
            room_instance.save()

        return hotel

