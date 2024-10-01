print(" -- signals.py is loaded -- ")

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import redis
from .models import Question


def clear_question_cache():
    import redis


def clear_question_cache():
    # Подключение к Redis напрямую
    r = redis.Redis(host="localhost", port=6379, db=0)

    # Сканируем все ключи
    cursor = 0
    all_keys = []
    while True:
        cursor, keys = r.scan(cursor)
        all_keys.extend(keys)
        if cursor == 0:
            break
    all_keys = [key.decode("utf-8") for key in all_keys]

    print("Все ключи в кеше:")
    for key in all_keys:
        print(key)
        r.delete(key)


@receiver(post_save, sender=Question)
def post_save_question(sender, instance, created, **kwargs):

    if instance.text:
        print("НОВЫЙ ВОПРОС")
        clear_question_cache()


@receiver(post_delete, sender=Question)
def pre_delete_question(sender, instance, **kwargs):
    print("ВОПРОС УДАЛЁН")
    clear_question_cache()
