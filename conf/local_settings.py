import os
from global_settings import PROJECT_PATH, INSTALLED_APPS, LOGGING

# Uncomment to put the application in non-debug mode. This is useful
# for testing error handling and messages.
# DEBUG = False
# TEMPLATE_DEBUG = DEBUG

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(PROJECT_PATH, 'apps.{{ project_name }}.db')
	}
}

INSTALLED_APPS += (
	'apps.base',
)

# Non-restricted email port for development, run in a terminal:
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_PORT = 1025
EMAIL_SUBJECT_PREFIX = '[{{ project_name }}] '

# This is used as a "seed" for various hashing algorithms. This must be set to
# a very long random string (40+ characters)
SECRET_KEY = '{{ secret_key }}'

# Uncomment for additional logging. If using the 'rotating_file' handler
# you must create the `logs` directory in the project root.
# LOGGING['handlers'].update({
#     'stdout': {
#         'class': 'logging.StreamHandler',
#         'level': 'DEBUG',
#     },
#     'rotating_file': {
#         'class': 'logging.handlers.RotatingFileHandler',
#         'level': 'DEBUG',
#         'filename': os.path.join(PROJECT_PATH, 'logs/debug.log')
#         'maxBytes': 2048,
#         'backupCount': 5,
#     },
# })
#
# LOGGING['loggers'].update({
#     'django.db.backends': {
#         'handlers': ['rotating_file'],
#         'propagate': True,
#         'level': 'DEBUG',
#     }
# })
