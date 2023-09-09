from http import HTTPStatus

from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import CreateModelMixin, ListModelMixin, \
    DestroyModelMixin
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from events.models import (City, Event, Favorite, Ticket, TypeEvent, TypeHall,
                           ZoneHall)

from .filters import CityFilter, EventFilter, EventSearch
from .permissions import IsAuthorStaffOrReadOnly
from .serializers import (CitySerializer, EventSerializer, FavoriteSerializer,
                          GetTicketSerializer, PostTicketSerializer,
                          TypeEventSerializer, TypeHallSerializer,
                          ZoneHallSerializer)


class TypeHallViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для типа схемы зала."""

    queryset = TypeHall.objects.all()
    serializer_class = TypeHallSerializer


class ZoneHallViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для зон схемы зала."""

    queryset = ZoneHall.objects.all()
    serializer_class = ZoneHallSerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для города."""
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_class = CityFilter


class TypeEventViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для типа мероприятия."""

    queryset = TypeEvent.objects.all()
    serializer_class = TypeEventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """Вьюсет для мероприятия."""

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend, EventSearch,)
    filterset_class = EventFilter
    search_fields = ('^name',)

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


class TicketViewSet(viewsets.ModelViewSet):
    """Вьюсет для билетов."""

    queryset = Ticket.objects.all()
    http_method_names = ['get', 'post']
    perimisson_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetTicketSerializer
        return PostTicketSerializer

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)


class FavoriteViewSet(viewsets.ViewSet):
    @action(
        methods=['POST'], detail=True, permission_classes=(IsAuthenticated,)
    )
    @transaction.atomic()
    def create(self, request, id=None):
        """Добавить в избранное событие."""
        user = request.user
        event = get_object_or_404(Event, id=id)
        data = {
            'user': user.id,
            'event': event.id,
        }
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        Favorite.objects.create(user=user, event=event)
        serializer = EventSerializer(event,
                                     context={'request': request})
        return Response(serializer.data, status=HTTPStatus.CREATED,
                        exception=True)

    @transaction.atomic()
    @action(
        methods=['DELETE'], detail=True,
        permission_classes=(IsAuthorStaffOrReadOnly,)
    )
    def destroy(self, request, id=None, ):
        """Удалить из избранного событие."""
        user = request.user
        try:
            event = Event.objects.filter(pk=id).first()
        except Event.DoesNotExist:
            raise serializers.ValidationError(
                'События не существует'
            )
        if not Favorite.objects.filter(user=user,
                                       event=event).first():
            raise serializers.ValidationError(
                'Событие не добавлено в избранное'
            )
        Favorite.objects.filter(user=user, event=event).delete()
        return Response(status=HTTPStatus.NO_CONTENT, exception=True)
