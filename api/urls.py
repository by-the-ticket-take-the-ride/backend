from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CityViewSet, EventViewSet, TypeEventViewSet

app_name = 'api'

router = DefaultRouter()

router.register('cities', CityViewSet, basename='cities')
router.register('types_event', TypeEventViewSet, basename='types_event')
router.register('events', EventViewSet, basename='events')
# router.register('favorite', FavoriteViewSet, basename='favotite')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
