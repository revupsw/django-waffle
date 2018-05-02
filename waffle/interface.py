from __future__ import unicode_literals

from decimal import Decimal
import random

from waffle.models import Flag
from waffle.utils import get_cache, get_setting, keyfmt

cache = get_cache()

class DoesNotExist(object):
    """The record does not exist."""
    @property
    def active(self):
        return get_setting('SWITCH_DEFAULT')


def set_flag(request, flag_name, active=True, session_only=False):
    """Set a flag value on a request object."""
    if not hasattr(request, 'waffles'):
        request.waffles = {}
    request.waffles[flag_name] = [active, session_only]


def _get_flag(flag_name):
    flag = cache.get(keyfmt(get_setting('FLAG_CACHE_KEY'), flag_name))
    if flag is None:
        try:
            flag = Flag.objects.get(name=flag_name)
        except Flag.DoesNotExist:
            flag = None
    return flag


def _flag_is_active_for_user(flag, user=None, **kwargs):
    if flag.staff and user.is_staff:
        return True

    if flag.superusers and user.is_superuser:
        return True

    flag_users = cache.get(keyfmt(get_setting('FLAG_USERS_CACHE_KEY'),
                                  flag.name))

    if flag_users is None:
        flag_users = flag.users.all()
    if user in flag_users:
        return True

    flag_groups = cache.get(keyfmt(get_setting('FLAG_GROUPS_CACHE_KEY'),
                                   flag.name))
    if flag_groups is None:
        flag_groups = flag.groups.all()
    user_groups = user.groups.all()
    for group in flag_groups:
        if group in user_groups:
            return True


def _flag_is_active_for_request(flag, flag_name=None, request=None, **kwargs):
    if get_setting('OVERRIDE'):
        if flag_name in request.GET:
            return request.GET[flag_name] == '1'

    if flag.testing:  # Testing mode is on.
        tc = get_setting('TEST_COOKIE') % flag_name
        if tc in request.GET:
            on = request.GET[tc] == '1'
            if not hasattr(request, 'waffle_tests'):
                request.waffle_tests = {}
            request.waffle_tests[flag_name] = on
            return on
        if tc in request.COOKIES:
            return request.COOKIES[tc] == 'True'

    user = request.user
    if flag.authenticated and user.is_authenticated():
        return True

    if flag.languages:
        languages = flag.languages.split(',')
        if (hasattr(request, 'LANGUAGE_CODE') and
                    request.LANGUAGE_CODE in languages):
            return True

    if flag.percent and flag.percent > 0:
        if not hasattr(request, 'waffles'):
            request.waffles = {}
        elif flag_name in request.waffles:
            return request.waffles[flag_name][0]

        cookie = get_setting('COOKIE') % flag_name
        if cookie in request.COOKIES:
            flag_active = (request.COOKIES[cookie] == 'True')
            set_flag(request, flag_name, flag_active, flag.rollout)
            return flag_active

        if Decimal(str(random.uniform(0, 100))) <= flag.percent:
            set_flag(request, flag_name, True, flag.rollout)
            return True
        set_flag(request, flag_name, False, flag.rollout)


def _flag_is_active(flag, **kwargs):
    if flag.everyone:
        return True
    elif flag.everyone is False:
        return False


def _flag_worker(flag_name_, functions, **kwargs):
    flag = _get_flag(flag_name_)
    if flag is None:
        return get_setting('FLAG_DEFAULT')
    else:
        for function in functions:
            result = function(flag, **kwargs)
            if result is not None:
                return result
        return False


def flag_is_active_for_user(user, flag_name):
    return _flag_worker(flag_name,
                        [_flag_is_active, _flag_is_active_for_user],
                        user=user)


def flag_is_active_for_request(request, flag_name):
    return _flag_worker(flag_name,
                        [_flag_is_active, _flag_is_active_for_request],
                        request=request, flag_name=flag_name)


def flag_is_active(request, flag_name):
    user = request.user
    return _flag_worker(flag_name,
                        [_flag_is_active, _flag_is_active_for_user,
                         _flag_is_active_for_request],
                        user=user, request=request, flag_name=flag_name)


def switch_is_active(switch_name):
    from .models import Switch

    switch = cache.get(keyfmt(get_setting('SWITCH_CACHE_KEY'), switch_name))
    if switch is None:
        try:
            switch = Switch.objects.get(name=switch_name)
        except Switch.DoesNotExist:
            switch = DoesNotExist()
            switch.name = switch_name
    return switch.active


def sample_is_active(sample_name):
    from .models import Sample

    sample = cache.get(keyfmt(get_setting('SAMPLE_CACHE_KEY'), sample_name))
    if sample is None:
        try:
            sample = Sample.objects.get(name=sample_name)
        except Sample.DoesNotExist:
            return get_setting('SAMPLE_DEFAULT')

    return Decimal(str(random.uniform(0, 100))) <= sample.percent
