from rest_framework import viewsets

from events.models import Event, TypeEvent

from .serializers import (EventSerializer, TypeEventSerializer,
                          FavoriteSerializer)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from http import HTTPStatus


class TypeEventViewSet(viewsets.ModelViewSet):
    """Вьюсет для типа мероприятия."""
    queryset = TypeEvent.objects.all()
    serializer_class = TypeEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """Вьюсет для мероприятия."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        """Добавление мероприятия в избранное."""
        data = {'user': request.user.id, 'event': pk}
        serializer = FavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)
