# Generated by Django 4.2.1 on 2023-08-10 11:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Город', max_length=50, unique=True, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название мероприятия', max_length=200, verbose_name='Название мероприятия')),
                ('description', models.CharField(help_text='Описание мероприятия', max_length=500, verbose_name='Описание мероприятия')),
                ('date_event', models.DateField(help_text='Дата мероприятия', verbose_name='Дата мероприятия')),
                ('time_event', models.TimeField(help_text='Время мероприятия', verbose_name='Время мероприятия')),
                ('image', models.ImageField(help_text='Изображение мероприятия', upload_to='events/', verbose_name='Изображение мероприятия')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(help_text='Автор мероприятия', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор мероприятия')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='TypeEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Тип мероприятия', max_length=50, unique=True, verbose_name='Тип мероприятия')),
                ('slug', models.SlugField(help_text='Слаг типа мероприятия', unique=True, verbose_name='Слаг типа мероприятия')),
            ],
            options={
                'verbose_name': 'Тип мероприятия',
                'verbose_name_plural': 'Типы мероприятий',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')),
                ('event', models.ForeignKey(help_text='Мероприятие', on_delete=django.db.models.deletion.CASCADE, to='events.event', verbose_name='Мероприятие')),
                ('user', models.ForeignKey(help_text='Покупатель', on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Билет',
                'verbose_name_plural': 'Билеты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название площадки', max_length=50, unique=True, verbose_name='Название площадки')),
                ('address', models.CharField(help_text='Адрес площадки', max_length=50, verbose_name='Адрес площадки')),
                ('city', models.ForeignKey(help_text='Город', on_delete=django.db.models.deletion.CASCADE, related_name='places', to='events.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Место мероприятия',
                'verbose_name_plural': 'Места мероприятий',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='events.event', verbose_name='Мероприятие')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Избранное мероприятие',
                'verbose_name_plural': 'Избранные мероприятия',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(help_text='Место мероприятия', on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.place', verbose_name='Место мероприятия'),
        ),
        migrations.AddField(
            model_name='event',
            name='type_event',
            field=models.ForeignKey(help_text='Тип мероприятия', on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.typeevent', verbose_name='Тип мероприятия'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'event'), name='unique_favourites'),
        ),
    ]