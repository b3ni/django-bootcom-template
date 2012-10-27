from conf.global_settings import *

try:
    from conf.local_settings import *
except ImportError:
    import warnings
    warnings.warn('Local settings have not been found')
