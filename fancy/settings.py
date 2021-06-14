from django.conf import settings
from getter import get_setting

DEBUG = settings.DEBUG
TYPE_CASTING = get_setting('FANCY', 'TYPE_CASTING')
RESERVED_PARAMS = get_setting('FANCY', 'RESERVED_PARAMS')
