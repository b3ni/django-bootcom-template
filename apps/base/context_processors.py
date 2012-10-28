import os
from django.conf import settings


def static(request):
    "Shorthand static URLs. In debug mode, the JavaScript is not minified."
    static_url = settings.STATIC_URL
    prefix = 'src' if settings.DEBUG else 'min'
    return {
        'BOOTSTRAP_URL': os.path.join(static_url, 'bootstrap'),
        'STYLES_URL': os.path.join(static_url, 'stylesheets'),
        'IMAGES_URL': os.path.join(static_url, 'images'),
        'SCRIPT_URL': os.path.join(static_url, 'scripts', prefix),
    }
