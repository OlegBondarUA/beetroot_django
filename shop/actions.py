import logging
from threading import Thread

from django.db.models import Model

from deep_translator import GoogleTranslator


translator = GoogleTranslator('en', 'uk')

logger = logging.getLogger('logit')


def translate_product(modeladmin, request, queryset):
    for obj in queryset:
        Thread(target=translate_object, args=(obj,)).start()


def translate_object(obj: Model):
    translate_list = [obj.title, obj.description]
    translated = translator.translate_batch(translate_list)

    obj.title_ua = translated[0]
    obj.description_ua = translated[1]
    obj.save()
    logger.info(f'HELLO - {obj.title_ua}')


translate_product.short_description = 'Translate Product'
