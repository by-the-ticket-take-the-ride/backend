from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from events.models import Event, TypeEvent, Favorite


class TypeEventSerializer(serializers.ModelSerializer):
    """Серилизатор типа мероприятия."""
    class Meta:
        model = TypeEvent
        fields = ('id', 'name', 'slug')


class EventSerializer(serializers.ModelSerializer):
    """Серилизатор мероприятия."""
    type_event = TypeEventSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'id',
            'type_event',
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


class FavoriteSerializer(serializers.ModelSerializer):
    "Сериализатор избранного."
    class Meta:
        model = Favorite
        fields = '__all__'
