from http import HTTPStatus

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import City, Event, Favorite, TypeEvent

from .filters import CityFilter, EventFilter
from .serializers import (CitySerializer, EventSerializer, FavoriteSerializer,
                          TypeEventSerializer)


class CityViewSet(viewsets.ModelViewSet):
    """Вьюсет для города."""
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_class = CityFilter


class TypeEventViewSet(viewsets.ModelViewSet):
    """Вьюсет для типа мероприятия."""
    queryset = TypeEvent.objects.all()
    serializer_class = TypeEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """Вьюсет для мероприятия."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

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
        user = request.user
        event = get_object_or_404(Event, id=pk)
        favorite = get_object_or_404(Favorite,
                                     user=user,
                                     event=event)
        favorite.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
