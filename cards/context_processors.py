from .translation import get_translation


def translations(request):
    """
    Контекст-процессор, который добавляет в контекст шаблонов переменную `t` —
    словарь переводов для текущего языка (берётся из сессии).

    Благодаря этому в шаблонах можно писать `{{ t.label.last_name }}` и т.д.
    """
    lang = request.session.get('language', 'ru')
    return {'t': get_translation(lang)}