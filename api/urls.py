from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CityViewSet, EventViewSet, TicketViewSet, TypeEventViewSet,
                    TypeHallViewSet, ZoneHallViewSet, FavoriteViewSet)

app_name = 'api'

router = DefaultRouter()

router.register('cities', CityViewSet, basename='cities')
router.register('types_event', TypeEventViewSet, basename='types_event')
router.register('events', EventViewSet, basename='events')
router.register('hall_types', TypeHallViewSet, basename='hall_types')
router.register('zones_hall', ZoneHallViewSet, basename='zones_hall')
router.register('tickets', TicketViewSet, basename='tickets')
# router.register('favorite', FavoriteViewSet, basename='favotite')

urlpatterns = [
    path('events/<int:id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'destroy',
                                  }), name='favorite'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
