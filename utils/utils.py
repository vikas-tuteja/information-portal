import contextlib
from functools import reduce
from django.core.exceptions import ValidationError

def getattr_recursive(obj: object, attributes: list, default=None):
    final_value = reduce(getattr_safe, [obj] + attributes)
    # Because 0 and False are valid return values
    if final_value is None:
        return default
    return final_value


def getattr_safe(obj, attr):
    with contextlib.suppress(AttributeError, ValueError):
        if isinstance(obj, dict):
            return obj.get(attr)
        elif isinstance(obj, (tuple, list)):
            with contextlib.suppress(IndexError):
                return obj[int(attr)]
        else:
            return getattr(obj, attr)


def validate_summary_len(val, min_len=180):
    if len(val) < min_len:
        raise ValidationError(
            'Summary Field length should be minimum {} \
                characters'.format(min_len))


