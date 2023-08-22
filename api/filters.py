from django_filters.rest_framework import FilterSet, filters

from events.models import City, Event


class EventFilter(FilterSet):
    city_name = filters.CharFilter(
        field_name='place__city__name',
        lookup_expr='startswith'
    )

    class Meta:
        model = Event
        fields = ['city_name']


class CityFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = City
        fields = ('name',)
