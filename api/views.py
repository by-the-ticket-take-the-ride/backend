from http import HTTPStatus
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import (
    Event,
    TypeEvent,
    City,
    TypeHall,
    Favorite,
    ZoneHall,
    Ticket
)

from .serializers import (
    EventSerializer,
    TypeEventSerializer,
    CitySerialier,
    TypeHallSerializer,
    FavoriteSerializer,
    ZoneHallSerializer,
    GetTicketSerializer,
    PostTicketSerializer
)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для городов."""

    queryset = City.objects.all()
    serializer_class = CitySerialier


class TypeHallViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для типа схемы зала."""

    queryset = TypeHall.objects.all()
    serializer_class = TypeHallSerializer


class ZoneHallViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для зон схемы зала."""

    queryset = ZoneHall.objects.all()
    serializer_class = ZoneHallSerializer


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
        user = request.user
        event = get_object_or_404(Event, id=pk)
        favorite = get_object_or_404(Favorite,
                                     user=user,
                                     event=event)
        favorite.delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class TicketViewSet(viewsets.ModelViewSet):
    """Вьюсет для билетов."""

    queryset = Ticket.objects.all()
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetTicketSerializer
        return PostTicketSerializer
