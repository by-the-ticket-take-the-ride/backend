from django.shortcuts import render
from rest_framework import viewsets
from events.models import Type_event, Event
from .serializers import Type_eventSerializer, EventSerializer


class Type_eventViewSet(viewsets.ModelViewSet):
    """Вьюсет для типа мероприятия."""
    queryset = Type_event.objects.all()
    serializer_class = Type_eventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """Вьюсет для мероприятия."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

