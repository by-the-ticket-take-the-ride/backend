from django_filters.rest_framework import CharFilter, FilterSet, filters

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
