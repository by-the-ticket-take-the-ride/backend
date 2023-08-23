from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TypeEvent(models.Model):
    """Тип мероприятия."""
    name = models.CharField(
        max_length=50,
        verbose_name='Тип мероприятия',
        help_text='Тип мероприятия',
        unique=True
    )
    slug = slug = models.SlugField(
        max_length=50,
        verbose_name='Слаг типа мероприятия',
        help_text='Слаг типа мероприятия',
        unique=True
    )

    class Meta:
        verbose_name = 'Тип мероприятия'
        verbose_name_plural = 'Типы мероприятий'

    def __str__(self):
        return self.name


class City(models.Model):
    """Модель города."""
    name = models.CharField(
        max_length=100,
        verbose_name='Город',
        help_text='Город'
    )
    name_en = models.CharField(
        max_length=50,
        verbose_name='Город',
        help_text='Город'
    )

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'name_en'),
                name='unique_city',
            )
        ]

    def __str__(self):
        return self.name


class ZoneHall(models.Model):
    """Модель зон зала."""

    name = models.CharField(
        max_length=50,
        verbose_name='Зона зала',
        help_text='Зона зала',
        unique=True
    )
    row = models.PositiveSmallIntegerField(
        verbose_name='Ряды в зоне зала',
        help_text='Ряды в зоне зала'
    )
    seat = models.PositiveSmallIntegerField(
        verbose_name='Места в зоне зала',
        help_text='Места в зоне зала'
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Стоимость билетов в этой зоне',
        help_text='Стоимость билетов в этой зоне'
    )

    class Meta:
        verbose_name = 'Зоны зала'
        verbose_name_plural = 'Зоны залов'

    def __str__(self):
        return self.name


class TypeHall(models.Model):
    """Модель схемы зала."""

    name = models.CharField(
        max_length=50,
        verbose_name='Название схемы зала',
        help_text='Название схемы зала',
        unique=True
    )
    zone = models.ManyToManyField(
        ZoneHall,
        through='TypeZoneHall',
        verbose_name='Зона зала',
        help_text='Зона зала',
        related_name='zones'
    )
    max_hall_capacity = models.PositiveSmallIntegerField(
        verbose_name='Максимальная вместимость зала',
        help_text='Максимальная вместимость зала'
    )

    class Meta:
        verbose_name = 'Схема зала'
        verbose_name_plural = 'Схемы залов'

    def __str__(self):
        return self.name


class TypeZoneHall(models.Model):

    type = models.ForeignKey(TypeHall, on_delete=models.CASCADE)
    zones = models.ForeignKey(ZoneHall, on_delete=models.CASCADE)

    def __str__(self):
        return f'Схема зала - {self.type}, зона - {self.zones}'

    class Meta:
        verbose_name = 'Зоны зала'
        verbose_name_plural = 'Зоны залов'
        constraints = [
            models.UniqueConstraint(
                fields=('type', 'zones'),
                name='type_zoness'
            )
        ]


class Place(models.Model):
    """Модель места проведения мероприятия."""
    name = models.CharField(
        max_length=50,
        verbose_name='Название площадки',
        help_text='Название площадки',
        unique=True
    )
    address = models.CharField(
        max_length=50,
        verbose_name='Адрес площадки',
        help_text='Адрес площадки',
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='Город',
        help_text='Город',
        related_name='places'
    )
    type = models.ForeignKey(
        TypeHall,
        on_delete=models.CASCADE,
        verbose_name='Схема зала',
        help_text='Схема зала',
        related_name='hall_types'
    )

    class Meta:
        verbose_name = 'Место мероприятия'
        verbose_name_plural = 'Места мероприятий'

    def __str__(self):
        return self.name


class Event(models.Model):
    """Модель мероприятия."""
    type_event = models.ForeignKey(
        TypeEvent,
        on_delete=models.CASCADE,
        verbose_name='Тип мероприятия',
        help_text='Тип мероприятия',
        related_name='events'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name='events',
        verbose_name='Автор мероприятия',
        help_text='Автор мероприятия',
    )
    name = models.CharField(
        verbose_name='Название мероприятия',
        help_text='Название мероприятия',
        max_length=200,
    )
    description = models.CharField(
        verbose_name='Описание мероприятия',
        help_text='Описание мероприятия',
        max_length=500,
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        verbose_name='Место мероприятия',
        help_text='Место мероприятия',
        related_name='events'
    )
    date_event = models.DateField(
        verbose_name='Дата мероприятия',
        help_text='Дата мероприятия',
    )
    time_event = models.TimeField(
        verbose_name='Время мероприятия',
        help_text='Время мероприятия',
    )
    image = models.ImageField(
        verbose_name='Изображение мероприятия',
        help_text='Изображение мероприятия',
        upload_to='events/',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """Модель билета."""
    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Гость мероприятия',
        help_text='Гость мероприятия',
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Мероприятие',
        help_text='Мероприятие',
    )
    zone_hall = models.ForeignKey(
        ZoneHall,
        on_delete=models.CASCADE,
        related_name='zones_hall',
        verbose_name='Зона зала',
        help_text='Зона зала'
    )
    row = models.PositiveSmallIntegerField(
        verbose_name='Ряд',
        help_text='Ряд'
    )
    seat = models.PositiveSmallIntegerField(
        verbose_name='Место',
        help_text='Место'
    )
    price = models.PositiveSmallIntegerField(
        verbose_name='Стоимость',
        help_text='Стоимость'
    )
    is_paid = models.BooleanField(
        verbose_name='Оплачено',
        help_text='Оплачено'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата покупки',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('guest', 'row', 'seat'),
                name='unique_ticket',
            )
        ]

    def __str__(self):
        return f'{self.guest} купил билет на {self.event}'


class Favorite(models.Model):
    """Модель избранного мероприятия."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Покупатель'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Мероприятие'
    )

    class Meta:
        verbose_name = 'Избранное мероприятие'
        verbose_name_plural = 'Избранные мероприятия'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'event'),
                name='unique_favourites',
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.event}" в Избранное'
