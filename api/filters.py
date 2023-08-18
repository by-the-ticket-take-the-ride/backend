from events.models import Event
from django_filters.rest_framework import CharFilter, FilterSet


class EventFilter(FilterSet):
    """Фильтр для мероприятий."""

    type_event = CharFilter(method='get_types')

    class Meta:
        model = Event
        fields = ('type_event',)

    def get_types(self, queryset, field_name, value):
        if value:
            return queryset.filter(
                type_event__slug__in=(
                    self.request.query_params.getlist('type_event')
                )
            )
        return queryset
