from rest_framework import viewsets

from events.models import Event, TypeEvent, Favorite
from django.shortcuts import get_object_or_404

from .serializers import (EventSerializer, TypeEventSerializer,
                          FavoriteSerializer)
from rest_framework import serializers
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
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

    @extend_schema(responses={
                   '204': FavoriteSerializer})
    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[permissions.IsAuthenticated],
            serializer_class=FavoriteSerializer)
    def favorite(self, request, pk):
        """Добавление мероприятия в избранное.
           Удаление мероприятия из избранного.
        """
        if request.method == 'POST':
            data = {'user': request.user.id, 'event': pk}
            serializer = FavoriteSerializer(data=data)
            if Favorite.objects.filter(user=request.user.id,
                                       event=pk).exists():
                raise serializers.ValidationError('Уже в избранном')
            if serializer.is_valid():
                serializer.save()
                return Response(status=HTTPStatus.OK)
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
        if request.method == "DELETE":
            user = request.user
            event = get_object_or_404(Event, id=pk)
            favorite = get_object_or_404(Favorite,
                                         user=user,
                                         event=event)
            favorite.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
