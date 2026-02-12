from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Person
from .translation import get_translation


# Список людей — стандартный ListView от Django.
# - `model` указывает модель, из которой будет формироваться queryset
# - `template_name` — шаблон, который будет отображаться
# - `context_object_name` — имя переменной в шаблоне
# - `paginate_by` включает постраничную навигацию
class PersonListView(ListView):
    model = Person
    template_name = 'cards/person_list.html'
    context_object_name = 'people'
    paginate_by = 10

    def get_queryset(self):
        # Переопределяем queryset, чтобы добавить простую фильтрацию по параметру `q`
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            # Используем icontains для нечувствительного к регистру поиска
            queryset = queryset.filter(last_name__icontains=q) | queryset.filter(first_name__icontains=q)
        return queryset


# Создание и редактирование используют те же поля и шаблон — CreateView/UpdateView
# В get_form мы подставляем локализованные метки/placeholder'ы из собственного translation
class PersonCreateView(CreateView):
    model = Person
    fields = ['last_name', 'first_name', 'middle_name', 'birth_date', 'photo']
    template_name = 'cards/person_form.html'
    success_url = reverse_lazy('cards:person_list')

    def get_form(self, form_class=None):
        # Получаем стандартную форму и изменяем метки/placeholder в зависимости от языка
        form = super().get_form(form_class)
        lang = self.request.session.get('language', 'ru')
        t = get_translation(lang)
        labels = t.get('label', {}) if isinstance(t, dict) else {}
        # Устанавливаем label и placeholder для каждого поля, если оно присутствует
        if 'last_name' in form.fields:
            form.fields['last_name'].label = labels.get('last_name', form.fields['last_name'].label)
            form.fields['last_name'].widget.attrs.update({'placeholder': labels.get('last_name', form.fields['last_name'].label)})
        if 'first_name' in form.fields:
            form.fields['first_name'].label = labels.get('first_name', form.fields['first_name'].label)
            form.fields['first_name'].widget.attrs.update({'placeholder': labels.get('first_name', form.fields['first_name'].label)})
        if 'middle_name' in form.fields:
            form.fields['middle_name'].label = labels.get('middle_name', form.fields['middle_name'].label)
            form.fields['middle_name'].widget.attrs.update({'placeholder': labels.get('middle_name', form.fields['middle_name'].label)})
        if 'birth_date' in form.fields:
            form.fields['birth_date'].label = labels.get('birth_date', form.fields['birth_date'].label)
            form.fields['birth_date'].widget.attrs.update({'placeholder': labels.get('birth_date', form.fields['birth_date'].label)})
        if 'photo' in form.fields:
            form.fields['photo'].label = labels.get('photo', form.fields['photo'].label)
        return form


class PersonDetailView(DetailView):
    # DetailView показывает одну запись модели
    model = Person
    template_name = 'cards/person_detail.html'
    context_object_name = 'person'


class PersonUpdateView(UpdateView):
    # UpdateView похож на CreateView, повторяемства здесь допускается
    model = Person
    fields = ['last_name', 'first_name', 'middle_name', 'birth_date', 'photo']
    template_name = 'cards/person_form.html'
    success_url = reverse_lazy('cards:person_list')

    def get_form(self, form_class=None):
        # Тот же механизм локализации labels/placeholder'ов, что и в CreateView
        form = super().get_form(form_class)
        lang = self.request.session.get('language', 'ru')
        t = get_translation(lang)
        labels = t.get('label', {}) if isinstance(t, dict) else {}
        if 'last_name' in form.fields:
            form.fields['last_name'].label = labels.get('last_name', form.fields['last_name'].label)
            form.fields['last_name'].widget.attrs.update({'placeholder': labels.get('last_name', form.fields['last_name'].label)})
        if 'first_name' in form.fields:
            form.fields['first_name'].label = labels.get('first_name', form.fields['first_name'].label)
            form.fields['first_name'].widget.attrs.update({'placeholder': labels.get('first_name', form.fields['first_name'].label)})
        if 'middle_name' in form.fields:
            form.fields['middle_name'].label = labels.get('middle_name', form.fields['middle_name'].label)
            form.fields['middle_name'].widget.attrs.update({'placeholder': labels.get('middle_name', form.fields['middle_name'].label)})
        if 'birth_date' in form.fields:
            form.fields['birth_date'].label = labels.get('birth_date', form.fields['birth_date'].label)
            form.fields['birth_date'].widget.attrs.update({'placeholder': labels.get('birth_date', form.fields['birth_date'].label)})
        if 'photo' in form.fields:
            form.fields['photo'].label = labels.get('photo', form.fields['photo'].label)
        return form


class PersonDeleteView(DeleteView):
    # DeleteView использует POST для удаления и перенаправляет на список
    model = Person
    template_name = 'cards/person_confirm_delete.html'
    success_url = reverse_lazy('cards:person_list')
