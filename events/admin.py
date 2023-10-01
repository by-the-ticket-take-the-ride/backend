from django.contrib import admin

from .models import (City, Event, Favorite, Place, Ticket, TypeEvent, TypeHall,
                     TypeZoneHall, ZoneHall)


@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_event')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ZoneInLine(admin.StackedInline):
    model = TypeZoneHall


@admin.register(TypeHall)
class TypeHallAdmin(admin.ModelAdmin):
    inlines = [ZoneInLine]
    list_display = ('name', 'max_hall_capacity')


@admin.register(ZoneHall)
class ZonesHallAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'event', 'is_paid')
    list_editable = ('is_paid',)


# admin.site.register(City)
admin.site.register(Place)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Favorite)
