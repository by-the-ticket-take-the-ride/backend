from rest_framework import viewsets

from events.models import Event, TypeEvent

from .serializers import (EventSerializer, TypeEventSerializer,
                          ListEventsSerializer)


class TypeEventViewSet(viewsets.ModelViewSet):
    """Вьюсет для типа мероприятия."""
    queryset = TypeEvent.objects.all()
    serializer_class = TypeEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """Вьюсет для мероприятия."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ListEventsSerializer
        return EventSerializer
