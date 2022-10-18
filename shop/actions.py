import logging
from threading import Thread, Lock

from django.db.models import Model

from deep_translator import GoogleTranslator


translator = GoogleTranslator('en', 'uk')

logger = logging.getLogger('logit')

lock = Lock()


def translate_product(modeladmin, request, queryset):
    for obj in queryset:
        if not obj.title_ua or not obj.description_ua:
            Thread(target=translate_product_data, args=(obj,)).start()


translate_product.short_description = 'Translate Product'


def translate_product_data(obj: Model):
    try:
        with lock:
            translate_list = [obj.title, obj.description]
            translated = translator.translate_batch(translate_list)

            obj.title_ua = translated[0]
            obj.description_ua = translated[1]
            obj.save()
    except Exception as error:
        logger.error(f'{obj.title} -> {error}')


def translate_name(modeladmin, request, queryset):
    objects_list = []
    for obj in queryset:
        if not obj.name_ua:
            objects_list.append(obj)

    Thread(
        target=translate_name_data,
        args=(objects_list, modeladmin.model)
    ).start()


def translate_name_data(objects_list: list[Model], model: Model):
    objects_names_list = []
    try:
        translated = translator.translate_batch(
            [obj.name for obj in objects_list]
        )
        for obj, translated_name in zip(objects_list, translated):
            obj.name_ua = translated_name
            objects_names_list.append(obj)

        model.objects.bulk_update(objects_names_list, ['name_ua'])
    except Exception as error:
        logger.error(f'Translating name error -> {error}')
