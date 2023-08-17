from rest_framework import viewsets

from events.models import Event, TypeEvent, City, TypeHall

from .serializers import EventSerializer, TypeEventSerializer, CitySerialier, TypeHallSerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для городов."""
    queryset = City.objects.all()
    serializer_class = CitySerialier


class TypeHallViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для типа схемы зала."""
    queryset = TypeHall.objects.all()
    serializer_class = TypeHallSerializer


class TypeEventViewSet(viewsets.ModelViewSet):
    """Вьюсет для типа мероприятия."""
    queryset = TypeEvent.objects.all()
    serializer_class = TypeEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """Вьюсет для мероприятия."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
