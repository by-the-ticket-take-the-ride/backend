from django.contrib import admin
from .models import (City, Event, Favorite, Place, Ticket, TypeEvent, TypeHall,
                     TypeZoneHall, ZoneHall, )

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin


class ZoneHallResource(resources.ModelResource):

    class Meta:
        model = ZoneHall


class TypeHallResource(resources.ModelResource):
    zone = fields.Field(
        column_name='zone',
        attribute='zone',
        widget=widgets.ManyToManyWidget(ZoneHall, field='name', separator=',')
    )

    class Meta:
        model = TypeHall


class PlaceResource(resources.ModelResource):
    city = fields.Field(
        column_name='city',
        attribute='city',
        widget=widgets.ForeignKeyWidget(City, field='name'))
    type = fields.Field(
        column_name='type',
        attribute='type',
        widget=widgets.ForeignKeyWidget(TypeHall, field='name')
    )

    class Meta:
        model = Place


class EventResource(resources.ModelResource):
    type_event = fields.Field(
        column_name='type_event',
        attribute='type_event',
        widget=widgets.ForeignKeyWidget(TypeEvent, field='name'))
    place = fields.Field(
        column_name='place',
        attribute='place',
        widget=widgets.ForeignKeyWidget(Place, field='name'))

    class Meta:
        model = Event


class PlaceAdmin(ImportExportModelAdmin):
    resource_classes = [PlaceResource]


@admin.register(TypeEvent)
class TypeEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'date_event')
    resource_classes = [EventResource]

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ZoneInLine(admin.StackedInline):
    model = TypeZoneHall


@admin.register(TypeHall)
class TypeHallAdmin(ImportExportModelAdmin):
    inlines = [ZoneInLine]
    list_display = ('name', 'max_hall_capacity')
    resource_classes = [TypeHallResource]

@admin.register(ZoneHall)
class ZonesHallAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    resource_classes = [ZoneHallResource]

# admin.site.register(City)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Ticket)
admin.site.register(Favorite)
