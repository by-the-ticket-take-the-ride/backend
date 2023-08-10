from django.contrib import admin
from .models import Type_event, Event


@admin.register(Type_event)
class Type_eventAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_event')

