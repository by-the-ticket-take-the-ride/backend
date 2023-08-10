from django.db import models


class Type_event(models.Model):
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

class Event(models.Model):
    """Модель мероприятия."""
    type_event = models.ForeignKey(
        Type_event,
        on_delete=models.CASCADE,
        verbose_name='Тип мероприятия',
        help_text='Тип мероприятия',
        related_name='events'
    )
    name = models.CharField(
        verbose_name='Название мероприятия',
        help_text='Название мероприятия',
        max_length=200,
    )
    discription = models.CharField(
        verbose_name='Описание мероприятия',
        help_text='Описание мероприятия',
        max_length=500,
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
        upload_to='event/',
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
