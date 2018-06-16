from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment
from server import settings


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        # 'static': staticfiles_storage.url,
        'url': reverse,
        'base_dir': settings.BASE_DIR
    })
    return env
