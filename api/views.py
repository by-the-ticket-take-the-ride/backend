from rest_framework import viewsets

from events.models import Event, TypeEvent, Favorite
from django.shortcuts import get_object_or_404

from .serializers import (EventSerializer, TypeEventSerializer,
                          FavoriteSerializer)
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from http import HTTPStatus


class TypeEventViewSet(viewsets.ModelViewSet):
    """Вьюсет для типа мероприятия."""
    queryset = TypeEvent.objects.all()
    serializer_class = TypeEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """Вьюсет для мероприятия."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAuthenticated],
            serializer_class=FavoriteSerializer)
    def favorite(self, request, pk):
        """Добавление мероприятия в избранное."""
        if request.method == 'POST':
            data = {'user': request.user.id, 'event': pk}
            serializer = FavoriteSerializer(data=data)
            if Favorite.objects.filter(user=request.user.id,
                                       event=pk).exists():
                raise serializers.ValidationError('Уже в избранном')
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=HTTPStatus.OK)
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаление мероприятия из избранного."""
        user = request.user
        event = get_object_or_404(Event, id=pk)
        favorite = get_object_or_404(Favorite,
                                     user=user,
                                     event=event)
        favorite.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
