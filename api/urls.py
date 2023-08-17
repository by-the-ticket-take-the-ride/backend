from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, TypeEventViewSet, CityViewSet, TypeHallViewSet

app_name = 'api'

router = DefaultRouter()

router.register('types_event', TypeEventViewSet, basename='types_event')
router.register('events', EventViewSet, basename='events')
router.register('city', CityViewSet, basename='cities')
router.register('hall_types', TypeHallViewSet, basename='hall_types')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
