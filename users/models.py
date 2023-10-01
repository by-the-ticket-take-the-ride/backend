from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField(
        max_length=150, unique=True, verbose_name='электронная почта'
    )
    username = models.CharField(max_length=50, verbose_name='имя пользователя')
    phone = models.CharField(
        max_length=12, null=True, blank=True, unique=True,
        validators=[RegexValidator(regex=r"^\+7\d{10}")],
        verbose_name='номер телефона',
        help_text='вводите номер в формате +7хххххххххх'
    )
    telegram = models.CharField(
        max_length=50, null=True, blank=True, unique=True,
        verbose_name='имя пользователя в Telegram'
    )
    is_organizer = models.BooleanField(default=False)
    birthday = models.DateField(verbose_name='Дата рождения', null=True,
                                blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        now = timezone.now().date()
        if self.birthday and self.birthday > (now - timedelta(days=365 * 18)):
            raise ValidationError(
                {'birthday': 'Пользователю должно быть больше 18 лет '})
        if self.birthday and (now.year - self.birthday.year) > 120:
            raise ValidationError({'birthday': 'Введите верный возраст'})
