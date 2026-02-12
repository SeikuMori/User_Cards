# Разбор кода проекта `django-person-card`

Документ собран для подготовки к зачёту — содержит понятные объяснения по ключевым файлам проекта, краткие ответы на возможные вопросы экзаменатора и указания, где в коде смотреть детали.

Файлы, разобранные здесь:
- `cards/models.py`
- `cards/views.py`
- `cards/urls.py`
- `cards/middleware.py`
- `cards/context_processors.py`
- `cards/admin.py`
- Шаблоны: `templates/cards/person_list.html`, `person_detail.html`, `person_form.html`, `person_confirm_delete.html`
- `personal_card_system/settings.py` (важные фрагменты)
- `manage.py`

---

**Как использовать этот документ**
- Сначала быстро просмотрите раздел «Ключевые вопросы и ответы» под каждым файлом — там типичные вопросы экзаменатора.
- Если нужно, откройте соответствующий файл в репозитории (`cards/...`) и посмотрите строку/функцию, на которую ссылается объяснение.

---

**`cards/models.py` — модель Person**

Краткая цель файла
- Описывает модель `Person`, используемую для хранения карточек людей (ФИО, дата рождения, фото).

Ключевые элементы и объяснение
- `cyrillic_validator` — объект `RegexValidator` для проверки ввода кириллицей (регулярное выражение `^[А-ЯЁа-яё\s-]+$`).
  - Зачем: гарантирует корректность данных (имена на русском), предотвращает нежелательные символы.
- `class Person(models.Model)` — класс модели, наследует `models.Model`.
  - `last_name`, `first_name`, `middle_name` — `CharField` с `validators=[RegexValidator(...)]`.
  - `birth_date` — `DateField` для хранения даты.
  - `photo` — `ImageField(upload_to='persons/')` указывает, что файлы будут сохраняться в `MEDIA_ROOT/persons/`.
- `def __str__(self)` — возвращает удобочитаемую строку, используется в админке и логах.
- `class Meta` — `verbose_name`, `verbose_name_plural`, `ordering`.

Типичные вопросы и ответы
- В: Почему используете `ImageField`?  
  О: `ImageField` автоматически хранит путь к файлу, интегрируется с настройками `MEDIA_ROOT`/`MEDIA_URL` и позволяет валидировать тип файла.
- В: Что даёт `validators` в поле?  
  О: Выполняет проверку значения поля до сохранения модели; если проверка не пройдена — форма покажет ошибку.
- В: Почему `middle_name` — `blank=True`?  
  О: Поле не обязательно; пользователю можно оставить отчество пустым.

---

**`cards/views.py` — представления (CBV)**

Краткая цель файла
- Определяет CRUD-интерфейс для модели `Person` с использованием generic class-based views (ListView, CreateView, DetailView, UpdateView, DeleteView).

Ключевые элементы и объяснение
- `PersonListView(ListView)`
  - `model = Person`, `template_name = 'cards/person_list.html'`, `context_object_name = 'people'`, `paginate_by = 10`.
  - `get_queryset(self)` — расширяет базовый queryset фильтрацией по `q` (GET-параметр): ищет по фамилии или имени (`icontains`).
  - Зачем: позволяет пользователю искать записи через поле поиска на странице списка.

- `PersonCreateView(CreateView)` и `PersonUpdateView(UpdateView)`
  - `fields` — поля формы, `template_name` и `success_url` заданы.
  - `get_form(self)` — получает форму, смотрит текущий язык в `request.session['language']`, берет словарь переводов через `get_translation` и подставляет `label` и `placeholder` для полей.
  - Зачем: реализует простую локализацию форм в рамках собственной реализации переводов.

- `PersonDetailView(DetailView)` — отображает одну запись (контекст `person`).
- `PersonDeleteView(DeleteView)` — подтверждение удаления + редирект на список.

Типичные вопросы и ответы
- В: Почему использованы class-based views (CBV), а не function-based views (FBV)?  
  О: CBV дают сокращение шаблонного кода: уже реализованы базовые операции (list/create/detail/update/delete) и легко переопределяются при необходимости.
- В: Что делает `reverse_lazy('cards:person_list')`?  
  О: Возвращает URL по имени маршрута; `reverse_lazy` используется в классовых атрибутах, чтобы обращение к URL происходило лениво (после загрузки конфигурации URL).
- В: Как реализована локализация меток формы?  
  О: Через собственную функцию `get_translation(lang)` (файл `cards/translation.py`) и обновление `form.fields[].label` и `widget.attrs['placeholder']`.

---

**`cards/urls.py` — маршруты (routes)**

Краткая цель
- Регистрирует URL'ы приложения `cards` и даёт им имена для удобного обратного разрешения.

Ключевые маршруты
- `path('', views.PersonListView.as_view(), name='person_list')` — главная страница списка.
- `path('add/', ...)`, `path('<int:pk>/', ...)`, `path('<int:pk>/edit/', ...)`, `path('<int:pk>/delete/', ...)` — CRUD.

Типичные вопросы
- В: Что такое `app_name = 'cards'`?  
  О: Пространство имён для URL-имен; позволяет использовать `{% url 'cards:person_list' %}` в шаблонах.

---

**`cards/middleware.py` — LocaleMiddleware**

Краткая цель
- Простая middleware, которая читает GET-параметр `lang` и сохраняет выбор языка в сессии (`request.session['language']`). Текущее значение кладёт в `request.LANGUAGE`.

Пояснения
- `__call__(self, request)` — здесь мы читаем `request.GET.get('lang')`, при наличии параметра — сохраняем в сессии.
- Используется в `MIDDLEWARE` (см. `settings.py`), поэтому выполняется для каждого запроса.

Вопросы
- В: Почему не использован встроенный `LocaleMiddleware` Django?  
  О: Проект использует упрощённый механизм переключения языка через GET/сессию, полного i18n-цикла не требуется.

---

**`cards/context_processors.py` — translations**

Краткая цель
- Добавляет в контекст шаблонов переменную `t`, содержащую словарь переводов для текущего языка.

Как это работает
- `lang = request.session.get('language', 'ru')`
- `return {'t': get_translation(lang)}` — шаблоны получают `{{ t.label.last_name }}` и т.д.

Вопросы
- В: Почему нужен context_processor, а не просто передавать `t` из view?  
  О: Контекст-процессор делает `t` доступным во всех шаблонах автоматически, без изменения всех view.

---

**`cards/admin.py` — админская конфигурация**

Ключевые элементы
- `@admin.register(Person)` и класс `PersonAdmin(admin.ModelAdmin)`.
- `list_display`, `list_filter`, `search_fields`, `ordering` — конфигурация списка записей.
- `fieldsets` — группировка полей в форме редактирования.
- `photo_preview(self, obj)` — метод, возвращающий HTML с превью изображения; используется в `readonly_fields`.

Вопросы
- В: Как безопасно вернуть HTML в админке?  
  О: Используется `format_html`, который экранирует параметры и помечает строку как безопасную.

---

**Шаблоны (`templates/cards/*.html`)**

Общие наблюдения
- Шаблоны используют `django_bootstrap5` для удобного рендера форм и Bootstrap-стилей.
- Переменная `t` используется для подстановки переводимых строк.

`person_list.html` — список с поиском и пагинацией
- Используются переменные `people`, `is_paginated`, `page_obj`, `paginator`.
- Форма поиска: `input name="q"` и `PersonListView.get_queryset` синхронизированы.
- В таблице ссылки на просмотр/редактирование/удаление.

`person_detail.html` — показывает фото (если есть) и данные.

`person_form.html` — форма создания/редактирования
- Поле `photo` реализовано через скрытый `<input type="file">` и пользовательский UI; есть JS, который показывает имя выбранного файла.

`person_confirm_delete.html` — подтверждение удаления (форма POST + CSRF).

Вопросы
- В: Почему форма удаления использует POST, а не GET?  
  О: По безопасности — операции, изменяющие состояние (удаление), должны выполняться через POST.
- В: Где хранится файл фото и как он отдаётся?  
  О: В `MEDIA_ROOT`; для разработки Django может отдавать их сам, в продакшене — через Nginx/CDN.

---

**`personal_card_system/settings.py` — важные настройки**

Что обратить внимание на (в этом проекте)
- `INSTALLED_APPS` включает `django_bootstrap5` и `cards.apps.CardsConfig`.
- `MIDDLEWARE` содержит `cards.middleware.LocaleMiddleware` — обеспечивает сохранение языка в сессии.
- `DATABASES` настроен на PostgreSQL (`ENGINE = 'django.db.backends.postgresql'`).
- `DEBUG = False` — в репозитории установлен в False (важно при запуске локально переключать в True для отладки).
- `STATICFILES_DIRS`, `STATIC_ROOT`, `MEDIA_ROOT`, `MEDIA_URL` — статические и медиа-файлы.

Вопросы
- В: Почему `DEBUG=False` в репозитории?  
  О: Безопасная практика, но для локальной разработки можно временно включить `DEBUG=True`.
- В: Как подключить статику в продакшене?  
  О: Выполнить `collectstatic`, настроить Nginx/сервис отдачи статики, использовать `STATIC_ROOT`.

---

**`manage.py`**

Коротко
- Стандартный исполняемый скрипт Django для запуска `manage.py` команд (migrations, runserver, shell и т.д.).
- Важная строка: `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_card_system.settings')` — указывает Django, какие настройки использовать.

Вопросы
- В: Как запустить сервер разработки?  
  О: `python manage.py runserver` (локально), для production — использовать Gunicorn/ASGI-решение через WSGI/ASGI и проксирование через Nginx.

---

**Итог / Что предоставить на зачёте**
- Знайте логику модели `Person` и почему выбраны типы полей.
- Уметь объяснить CRUD-поток: какой view отвечает за создание, где задаются поля формы, как работает редирект (`success_url`).
- Понимать, как работает локализация через `LocaleMiddleware` + `context_processors.translations` + `get_translation`.
- Быть готовым показать, где и почему применяются валидации (`RegexValidator`) и как тестировать их через админку/формы.

Если нужно, я могу:
- Сгенерировать отдельный список «вопросов экзаменатора» (5–10 вопросов с короткими ответами) для каждого файла.
- Преобразовать этот документ в PDF для печати.
- Добавить ещё более детальные построчные комментарии прямо в те файлы, которые вы укажете.

---

*Документ сгенерирован автоматически. Если хотите — могу расширить любой раздел и добавить ссылки на конкретные строки в репозитории (формат: `file:line`), или создать краткую «шпаргалку» (1 страница) с ключевыми фразами.*
