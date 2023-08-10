from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from event.models import Type_event, Event


class Type_eventSerializer(serializers.ModelSerializer):
    """Серилизатор типа мероприятия."""
    class Meta:
        model = Type_event
        fields = ('id', 'name', 'slug')


class EventSerializer(serializers.ModelSerializer):
    """Серилизатор мероприятия."""
    type_event = Type_eventSerializer(read_only=True)
    image = Base64ImageField()
    class Meta:
        model = Event
        fields = (
            'id',
            'type_event',
            'name',
            'discription',
            'date_event',
            'time_event',
            'image',            
        )