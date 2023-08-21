from http import HTTPStatus

import requests
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from ipware import get_client_ip
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from events.models import Event, Favorite, TypeEvent

from .filters import EventFilter
from .serializers import (EventSerializer, FavoriteSerializer,
                          TypeEventSerializer)


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

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        # Определение города по IP-адресу
        client_ip, _ = get_client_ip(self.request)
        response = requests.get(f'http://ipinfo.io/{client_ip}/json')
        data = response.json()
        city_name_ip = data.get('city', '')

        # Получение города из параметра запроса
        city_name_query = self.request.query_params.get('city_name', '')

        if city_name_query:
            queryset = queryset.filter(
                place__city__name__iexact=city_name_query)
        elif city_name_ip:
            queryset = queryset.filter(
                place__city__name_en__iexact=city_name_ip)

        return queryset

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
