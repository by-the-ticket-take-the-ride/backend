import requests
from django_filters.rest_framework import FilterSet, filters
from ipware import get_client_ip

from events.models import City, Event


class CityFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = City
        fields = ('name',)


class EventFilter(FilterSet):
    """Фильтр для мероприятий."""

    type_event = filters.CharFilter(method='get_types')
    city_name = filters.CharFilter(method='get_city_name')

    class Meta:
        model = Event
        fields = ('type_event', 'city_name')

    def get_types(self, queryset, field_name, value):
        if value:
            return queryset.filter(
                type_event__slug__in=(
                    self.request.query_params.getlist('type_event')
                )
            )
        return queryset

    def get_city_name(self, queryset, field_name, value):
        if value:
            return queryset.filter(
                place__city__name__startswith=value.lower().capitalize())
        return queryset

    def filter_queryset(self, queryset):
        # Определение города по IP-адресу
        client_ip, _ = get_client_ip(self.request)
        response = requests.get(f'http://ipinfo.io/{client_ip}/json')
        data = response.json()
        city_name_ip = data.get('city', '')

        # Получение города из параметра запроса
        city_name_query = self.request.query_params.get('city_name', '')

        if city_name_query:
            self.get_city_name(queryset, 'city_name', city_name_query)
        elif city_name_ip:
            queryset = queryset.filter(
                place__city__name_en__iexact=city_name_ip)

        return super().filter_queryset(queryset)
