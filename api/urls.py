from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, TypeEventViewSet

app_name = 'api'

router = DefaultRouter()

router.register('types_event', TypeEventViewSet, basename='types_event')
router.register('events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]
