from django.contrib import admin
from .models import TypeEvent, Event, Ticket, Favorite, Place, City


@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_event')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# admin.site.register(City)
admin.site.register(Place)
admin.site.register(Ticket)
admin.site.register(Favorite)