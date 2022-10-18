from django import template
from django.conf import settings


register = template.Library()


@register.filter(name="switch_i18n")
def switch_i18n(request, language):
    """takes in a request object and gets the path from it"""

    path = request.get_full_path()
    lang_codes = [c for (c, name) in settings.LANGUAGES]
    lang_codes.append('default')
    if language not in lang_codes:
        raise Exception(f'{language} is not a supported language code')
    parts = path.split('/')
    if parts[1] in lang_codes:
        if language == 'default':
            del parts[1]
        else:
            parts[1] = language
    else:
        if language != 'default':
            parts[0] = "/" + language
    return '/'.join(parts)
