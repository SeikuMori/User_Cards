from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'birth_date')
    search_fields = ('last_name', 'first_name')
    list_filter = ('birth_date',)