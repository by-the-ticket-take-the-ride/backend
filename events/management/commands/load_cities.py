import csv
import logging

from django.core.management.base import BaseCommand

from events.models import City

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.import_cities()
        logging.info('Загрузка городов завершена.')

    def import_cities(self, file='cities.csv'):
        logging.info(f'Загрузка {file}...')
        file_path = f'./data/{file}'
        with open(file_path, newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Пропускаем заголовок
            for row in csv_reader:
                name = row[2]
                name_en = row[1]
                City.objects.update_or_create(name=name, name_en=name_en)
