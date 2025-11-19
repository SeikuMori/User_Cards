from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

cyrillic_validator = RegexValidator(
    regex=r'^[А-ЯЁа-яё\s-]+$',
    message='Разрешены только русские буквы, пробел и дефис'
)

class Person(models.Model):
    last_name = models.CharField(
        max_length=50,
        validators=[cyrillic_validator],
        verbose_name='Фамилия'
    )
    first_name = models.CharField(
        max_length=50,
        validators=[cyrillic_validator],
        verbose_name='Имя'
    )
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[cyrillic_validator],
        verbose_name='Отчество'
    )
    birth_date = models.DateField(verbose_name='Дата рождения')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Карточка человека'
        verbose_name_plural = 'Карточки людей'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

# Create your models here.
