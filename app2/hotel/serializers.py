from rest_framework import serializers
from core.models import Hotel, Room

class RoomSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Room
        fields = ('id', 'room_number', 'price', 'type')

class HotelSerializers(serializers.ModelSerializer):

    rooms = RoomSerializers(many=True)
    class Meta:
        model = Hotel
        fields = '__all__'

    def validate(self, attr):
        rooms_date = attr.get('rooms', None)
        room_numbers = [room['room_number'] for room in rooms_date]

        if len(room_numbers) != len(set(room_numbers)):
            raise serializers.ValidationError({'room_number': 'Room numbers must be unique over a hotel room!'})

        return attr

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms' , None)
        hotel = Hotel.objects.create(**validated_data)
        for room_data in rooms_data:
            Room.objects.create(hotel=hotel, **room_data)

        return hotel

    def update(self, instance, validated_data):
        rooms_date = validated_data.pop('rooms', None)
        hotel = super().update(instance, validated_data)
        for room_date in rooms_date:
            room_instance = Room.objects.get(id=room_date.pop('id', None))

            # validate room_number

            update_room_number = room_date.get('room_number')
            if update_room_number and room_instance.room_number != update_room_number:
                all_room_numbers = [room.room_number for room in Room.objects.filter(hotel=hotel)]
                if all_room_numbers.__contains__(update_room_number):
                    raise serializers.ValidationError({'room_number': 'Room numbers must be unique over a hotel room!'})

            #

            room_serializer = RoomSerializers(instance=room_instance, data=room_date, partial=True)
            if room_serializer.is_valid():
                room_serializer.save()
            else:
                raise serializers.ValidationError(room_serializer.errors)

#           room_instance.update(room_date)
#           room_instance.save()

        return hotel

class HotelImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('id', 'image')
        read_only = ('id', )