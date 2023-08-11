import os
import json

from django.core.management.base import BaseCommand, CommandError
from events.models import TypeEvent, City
from wiki.settings import TEST_DATA_DIR


class Command(BaseCommand):
    help = 'Read or write from json to DB.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--read_cities',
            action='store_true',
            help='read from database',
        )
        parser.add_argument(
            '--write_cities',
            action='store_true',
            help='read from database',
        )
        parser.add_argument(
            '--write_types',
            action='store_true',
            help='write json data to database',
        )
        parser.add_argument(
            '--read_types',
            action='store_true',
            help='write json data to database',
        )

    def write_cities(self, data):
        for obj in data:
            City.objects.get_or_create(**obj)
        self.stdout.write('Данные о городах успешно импортированы.')

    def read_cities(self):
        for obj in City.objects.all():
            print(obj, end='\n')
        self.stdout.write('Данные о городах успешно прочитаны.')

    def write_types(self, data):
        for obj in data:
            TypeEvent.objects.get_or_create(**obj)
        self.stdout.write('Данные о типах успешно импортированы.')

    def read_types(self):
        for obj in TypeEvent.objects.all():
            print(obj, end='\n')
        self.stdout.write('Данные о типах успешно прочитаны.')

    def handle(self, **options):
        if not (
            options.get("read_cities")
            or options.get("write_cities")
            or options.get("write_types")
            or options.get("read_types")
            ):
            raise CommandError(
                'Use --read_cities or --write_cities or'
                '--write_types or --read_types argument'
            )
        if options['write_cities']:
            json_file = os.path.join(TEST_DATA_DIR, 'cities.json')
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.write_cities(data)
        if options['write_types']:
            json_file = os.path.join(TEST_DATA_DIR, 'types.json')
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.write_types(data)
        if options['read_cities']:
            self.read_cities()
        if options['read_types']:
            self.read_types()
