from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from events.models import City, Event, Favorite, Place, TypeEvent


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор города."""
    class Meta:
        model = City
        fields = ('id', 'name')


class TypeEventSerializer(serializers.ModelSerializer):
    """Серилизатор типа мероприятия."""
    class Meta:
        model = TypeEvent
        fields = ('id', 'name', 'slug')


class PlaceSerializer(serializers.ModelSerializer):
    """Сериализатор места мероприятия."""
    city = CitySerializer(read_only=True)

    class Meta:
        model = Place
        fields = ('id', 'name', 'address', 'city')


class EventSerializer(serializers.ModelSerializer):
    """Серилизатор мероприятия."""
    type_event = TypeEventSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    place = PlaceSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'type_event',
            'place',
            'name',
            'description',
            'date_event',
            'time_event',
            'image',
            'is_favorited',
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, event=obj
        ).exists()


@extend_schema_serializer(
    exclude_fields=(
        ['user', 'event']
    )
)
class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранного."""

    class Meta:
        model = Favorite
        fields = ('user', 'event')
