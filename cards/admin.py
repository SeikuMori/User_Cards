from django.contrib import admin
from django.utils.html import format_html
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """
    Конфигурация отображения модели Person в административной части Django.

    Обратите внимание на:
    - `list_display` — колонки в списке записей
    - `search_fields` и `list_filter` — удобные фильтры/поиск в админке
    - `fieldsets` — организация полей в форме редактирования
    - `readonly_fields` и метод `photo_preview` — показываем превью изображения
    """
    list_display = ('last_name', 'first_name', 'middle_name', 'birth_date')  # отображаемые колонки
    list_filter = ('last_name', 'birth_date')
    search_fields = ('last_name', 'first_name', 'middle_name')
    ordering = ('last_name', 'first_name')
    
    fieldsets = (
        (None, {
            'fields': ('last_name', 'first_name', 'middle_name')
        }),
        ('Дополнительно', {
            'fields': ('birth_date', 'photo'),
            'classes': ('collapse',)
        }),
    )
    
    # Чтобы фото отображалось в админке как превью — делаем поле только для чтения
    readonly_fields = ('photo_preview',)
    
    def photo_preview(self, obj):
        # Возвращаем HTML с тегом <img> — format_html защищает от XSS
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 200px; border-radius: 8px;">',
                obj.photo.url
            )
        return "(нет фото)"
    photo_preview.short_description = "Превью"