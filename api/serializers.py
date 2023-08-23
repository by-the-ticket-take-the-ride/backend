from drf_extra_fields.fields import Base64ImageField
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import exceptions, serializers

from events.models import (City, Event, Favorite, Place, Ticket, TypeEvent,
                           TypeHall, ZoneHall)
from users.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    """Данные о пользователе."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'telegram',)


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


class ZoneHallSerializer(serializers.ModelSerializer):
    """Сериализатор для зон схемы зала."""

    class Meta:
        model = ZoneHall
        fields = ('id', 'name', 'row', 'seat', 'price')


class TypeHallSerializer(serializers.ModelSerializer):
    """Сериализатор типа зала."""

    zone = ZoneHallSerializer(many=True, read_only=True)

    class Meta:
        model = TypeHall
        fields = ('id', 'name', 'zone', 'max_hall_capacity')


class PlaceSerializer(serializers.ModelSerializer):
    """Сериализатор площадки"""

    city = CitySerializer(read_only=True)
    type = TypeHallSerializer(read_only=True)

    class Meta:
        model = Place
        fields = ('id', 'name', 'address', 'city', 'type')


class EventSerializer(serializers.ModelSerializer):
    """Серилизатор мероприятия."""

    type_event = TypeEventSerializer(read_only=True)
    image = Base64ImageField()
    place = PlaceSerializer(read_only=True)
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


class GetTicketSerializer(serializers.ModelSerializer):
    """Сериализатор билетов метод GET."""

    guest = UserInfoSerializer(many=False, read_only=True)
    event = EventSerializer(many=False, read_only=True)
    zone_hall = ZoneHallSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'event',
            'zone_hall',
            'row',
            'seat',
            'price',
            'guest',
            'is_paid'
        )


class PostTicketSerializer(serializers.ModelSerializer):
    """Сериализатор билетов метод POST."""

    guest = UserInfoSerializer(
        many=False, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Ticket
        fields = (
            'id',
            'event',
            'zone_hall',
            'row',
            'seat',
            'guest',
            'is_paid'
        )

    def to_representation(self, instance):
        serializer = GetTicketSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise exceptions.NotAuthenticated(
                'Пользователь не авторизован.'
            )
        zone_hall = validated_data.get('zone_hall')
        validated_data['price'] = zone_hall.price
        if Ticket.objects.filter(
            guest=validated_data.get('guest'),
            row=validated_data.get('row'),
            seat=validated_data.get('seat')
        ).exists():
            raise serializers.ValidationError(
                'Билет уже куплен.'
            )
        return super().create(validated_data)
