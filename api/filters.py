from django_filters.rest_framework import CharFilter, FilterSet, filters
from rest_framework import serializers
from rest_framework.filters import SearchFilter

from events.models import City, Event


class EventFilter(FilterSet):
    """Фильтр для мероприятий."""

    type_event = CharFilter(method='get_types')
    city_name = filters.CharFilter(
        field_name='place__city__name',
        lookup_expr='startswith'
    )

    class Meta:
        model = Event
        fields = ('type_event', 'city_name',)

    def get_types(self, queryset, field_name, value):
        if value:
            return queryset.filter(
                type_event__slug__in=(
                    self.request.query_params.getlist('type_event')
                )
            )
        return queryset


class CityFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = City
        fields = ('name',)


class EventSearch(SearchFilter):
    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, '')
        if len(params) < 2 or len(params) > 100:
            raise serializers.ValidationError(
                'Количество символов в поле поиска должно быть от 2 до 100')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        return params.split()
