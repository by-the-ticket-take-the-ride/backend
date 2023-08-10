from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from events.models import TypeEvent, Event


class TypeEventSerializer(serializers.ModelSerializer):
    """Серилизатор типа мероприятия."""
    class Meta:
        model = TypeEvent
        fields = ('id', 'name', 'slug')


class EventSerializer(serializers.ModelSerializer):
    """Серилизатор мероприятия."""
    type_event = TypeEventSerializer(read_only=True)
    image = Base64ImageField()
    class Meta:
        model = Event
        fields = (
            'id',
            'type_event',
            'name',
            'description',
            'date_event',
            'time_event',
            'image',            
        )