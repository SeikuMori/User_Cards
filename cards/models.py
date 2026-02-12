from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Валидатор для полей, разрешающий только кириллические символы, пробел и дефис.
# Его можно применить к любым полям CharField, где требуется ввод на русском.
cyrillic_validator = RegexValidator(
    regex=r'^[А-ЯЁа-яё\s-]+$',
    message='Разрешены только русские буквы, пробел и дефис'
)


class Person(models.Model):
    """
    Модель `Person` соответствует записи (карточке) человека.

    Поля:
    - last_name, first_name, middle_name: строки с валидацией на кирлицу
    - birth_date: дата рождения
    - photo: загружаемое изображение (опционально)

    Методы и поведение:
    - __str__: удобное строковое представление для администратора и отладки
    - Meta: читаемые имена модели и порядок по умолчанию
    """

    # Поля модели — используются Django ORM для генерации схемы таблицы и форм
    last_name = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[А-ЯЁа-яё]+$', 'Фамилия должна содержать только кириллицу')],
        verbose_name="Фамилия"
    )
    first_name = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[А-ЯЁа-яё]+$', 'Имя должна содержать только кириллицу')],
        verbose_name="Имя"
    )
    # Отчество не обязательное (blank=True), но по необходимости тоже валидируется
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        validators=[RegexValidator(r'^[А-ЯЁа-яё]+$', 'Отчество должно содержать только кириллицу')],
        verbose_name="Отчество"
    )
    birth_date = models.DateField(verbose_name="Дата рождения")
    # ImageField хранит путь к файлу в MEDIA_ROOT; upload_to определяет подпапку
    photo = models.ImageField(
        upload_to='persons/',
        blank=True,
        null=True,
        verbose_name="Фотография"
    )

    def __str__(self):
        # Строковое представление используется в списках, админке и отладке
        return f"{self.last_name} {self.first_name}"

    class Meta:
        # Читаемые имена и сортировка по умолчанию
        verbose_name = "Человек"
        verbose_name_plural = "Люди"
        ordering = ['last_name', 'first_name']

# Конец файла models.py
