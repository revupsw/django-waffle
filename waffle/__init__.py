from waffle.utils import get_setting, keyfmt
from .interface import (
    DoesNotExist, set_flag, flag_is_active_for_user, flag_is_active,
    flag_is_active_for_request, switch_is_active, sample_is_active)

VERSION = (0, 11, 1)
__version__ = '.'.join(map(str, VERSION))
