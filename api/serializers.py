from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from events.models import Event, TypeEvent, Place, City, TypeHall


class TypeEventSerializer(serializers.ModelSerializer):
    """Серилизатор типа мероприятия."""
    class Meta:
        model = TypeEvent
        fields = ('id', 'name', 'slug')


class CitySerialier(serializers.ModelSerializer):
    """Сериализатор города."""

    class Meta:
        model = City
        fields = ('id', 'name')


class TypeHallSerializer(serializers.ModelSerializer):
    """Сериализатор типа зала."""

    class Meta:
        model = TypeHall
        fields = ('id', 'name', 'zone', 'row', 'seat')


class PlaceSerializer(serializers.ModelSerializer):
    """Сериализатор площадки"""

    city = CitySerialier(read_only=True)
    type = TypeHallSerializer(read_only=True)

    class Meta:
        model = Place
        fields = ('id', 'name', 'address', 'city', 'type', 'max_hall_capacity')


class EventSerializer(serializers.ModelSerializer):
    """Серилизатор мероприятия."""
    type_event = TypeEventSerializer(read_only=True)
    image = Base64ImageField()
    place = PlaceSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'type_event',
            'place',
            'name',
            'description',
            'date_event',
            'time_event',
            'image',
        )
