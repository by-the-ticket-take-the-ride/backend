from django_filters.rest_framework import FilterSet, filters
from events.models import Event


class EventFilter(FilterSet):
    city_name = filters.CharFilter(
        field_name='place__city__name',
        lookup_expr='startswith'
    )

    class Meta:
        model = Event
        fields = ['city_name']
