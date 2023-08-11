from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenCreateView, TokenDestroyView

from .views import TypeEventViewSet, EventViewSet


app_name = 'api'

router = DefaultRouter()

router.register('types_event', TypeEventViewSet, basename='types_event')
router.register('events', EventViewSet, basename='events')

urlpatterns = [
    path(r'login/', TokenCreateView.as_view(), name='login'),
    path(r'logout/', TokenDestroyView.as_view(), name='logout'),
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]
