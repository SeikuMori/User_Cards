class LocaleMiddleware:
    """
    Простая middleware для управления языком интерфейса через GET-параметр.

    Поведение:
    - если в GET есть параметр `lang`, он сохраняется в сессии как `language`
    - текущее значение языка сохраняется в `request.LANGUAGE` для использования в шаблонах/коде

    Это облегчает переключение языка в приложении без использования полного механизма i18n Django.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем GET-параметр 'lang' и сохраняем в сессию
        lang = request.GET.get('lang')
        if lang:
            request.session['language'] = lang.lower()
            # В dev удобно видеть в консоли — в проде лучше использовать логгер
            print(f"Language changed to {lang} — session updated")  # Дебаг
        # Берём язык из сессии, если нет — по умолчанию 'ru'
        lang = request.session.get('language', 'ru')
        request.LANGUAGE = lang
        print(f"Current language: {lang}")  # Дебаг
        response = self.get_response(request)
        return response