from django.test import TestCase
from json.decoder import JSONDecodeError


def check_dict_keys(subject, model):
    """
    check that each key in `model` is reflected in `subject`

    returns a dict mapping the 'bad' keys to the reason they are 'bad', or a
        similar dict for a nested layer

    specing guide:
    - The following steps are run in order
    - For every key in `subject` you wish to validate, include that `key` in
        `model`.
    - If the value at `key` in `model` is callable, it will be called, passing
        in the value at `key` in `subject. If it returns a Falsy value OR
        `True`, that key will be treated as correct. If a non-`True` truthy
        value is returned or an exception is raised, the `key` field will be
        marked as bad. If a truthy value was returned, this will be used as the
        reason string (even if it's not a string, it will become one when
        interpolated into the report). If an exception was raised, a generic
        'validation failed' message will be used with the exception info.
        * This allows for fuzzier checks, like regular expressions, or the
            is_absent helper
    - If they key is absent from `subject`, `key` will be marked as bad with an
        'absent' message
    - If the value at `key` in `model` is a dictionary, this will recurse,
        passing the value at `key` in `subject` and the dict in `model` at
        `key`.
    - Finally, if the value at `key` in `subject` is not (==) equivalent to the
        value at `key` in `model`, `key` will be marked as bad.


    :param subject dict: The dict object to compare to `model`
    :param model dict: The 'spec' dict object to which `subject` will be
        compared
    :returns dict: mapping of bad keys to reason string or dict of nested bad
        keys
    """
    bad_keys = {}

    for key, spec in model.items():
        # if a callable was passed, call it, passing the subject value
        if callable(spec):
            result = spec(subject.get(key, None))
            try:
                if result and result is not True:
                    bad_keys[key] = result
            except Exception as exc:
                bad_keys[key] = (
                    f'Failed Validation({exc.__class__.__name__}: {exc}'
                )
            continue

        try:
            value = subject[key]
        except KeyError:
            bad_keys[key] = f'Missing'
            continue

        # check for type mismatch
        if not isinstance(value, spec.__class__):
            bad_keys[key] = (
                f'wrong type: {value.__class__.__name__} '
                f'(expected {spec.__class__.__name__})'
            )
            continue

        # recursively check dicts
        if isinstance(spec, dict):
            bad_children = check_dict_keys(value, spec)
            if bad_children:
                bad_keys[key] = bad_children
                continue

        # handle arrays?

        if value != spec:
            bad_keys[key] = f'{value} != {spec}'

    return bad_keys


def print_bad_keys(bad_keys, indent_level=0, prefix='- '):
    """returns a list of line strings showing errors for the bad keys

    :param bad_keys dict: Dictionary mapping keys to reason messages or nested
        bad_key dict
    :param indent_level int: Nesting level of this iteration. 0 for top-level.
        default: 0
    :param prefix str: Prefix string to print after indentation but before the
        key on lines. default: '- '
    :returns list: of strings (lines to be printed in failure report)
    """
    line_prefix = ('  ' * indent_level) + prefix
    buffer = []
    for k, v in bad_keys.items():
        if isinstance(v, dict):
            buffer.append(f'{line_prefix}{k}:')
            buffer += print_bad_keys(
                v, indent_level=indent_level+1, prefix=prefix
            )
        else:
            buffer.append(f'{line_prefix}{k}: {v}')

    return buffer


class JSONTestCase(TestCase):
    """
    TestCase class that adds the assertContainsJSON method
    """
    def assertContainsJSON(
        self, response, spec, status_code=200, msg_prefix=""
    ):
        """
        Assert that the json body of `response` matches the spec given by
        `spec`, and that it's status code is correct.

        keys absent from `spec` will be ignored. This allows for partial
        matching.  works recursively too. If a dict is encountered at a spec'd
        key, the same checks will be done at that nested level too.

        Attempts to compose a highly readable error report too

        :param response : The test client response to test
        :param spec dict: spec for the body to test against
        :param status_code int: expected HTTP status code. Pass a falsy value
            to disable status_code check. default 200
        :param msg_prefix str: Message with which to prefix the error
            default: 'JSON Mismatch'
        :returns: a dict mapping erroneous field keys to a reason string or a
            similar dict for nested layers
        :raises AssertionError: if the status code is wrong or some keys are
            mismatched
        """

        if status_code and (response.status_code != status_code):
            try:
                content = response.json()
            except (ValueError, JSONDecodeError):
                content = response.content

            msg = (
                f"{(msg_prefix + ': ') if msg_prefix else ''}"
                f"Wrong status code: {response.status_code} != {status_code} : "
                f"(expected {status_code})\n"
                f"======:\n{content}"
            )
            raise AssertionError(msg)

        try:
            # handle non-json payloads
            content = response.json()
        except (ValueError, JSONDecodeError) as exc:
            msg = (
                f"{(msg_prefix + ': ') if msg_prefix else ''}"
                f"{exc.__class__.__name__} on json decode: "
                f"{exc}\n"
                f"======:\n{response.content}"
            )
            raise AssertionError(msg) from exc

        bad_keys = check_dict_keys(content, spec)
        if bad_keys:
            msg = (
                f"{(msg_prefix + ': ') if msg_prefix else ''}"
                f"Dict does not match spec on these keys:\n" +
                '\n'.join(print_bad_keys(bad_keys))
            )
            exc = AssertionError(msg)
            exc.bad_keys = bad_keys
            raise exc


JWT_REGEX = r'^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$'


def is_jwt(token):
    """Returns true if `token` is a JWT"""
    import re
    if re.match(JWT_REGEX, token):
        return True
    return "Not a JWT"


def is_absent(value=None):
    """Returns true if `value` is None"""
    if value is None:
        return True
    return f"Has a value where there should be none ({value})"


def is_datetime(value=None):
    from django.utils.dateparse import parse_datetime
    """Returns true if `value` is parseable to a datetime"""
    try:
        parse_datetime(value)
    except Exception:
        return False
    return True


class SpecHelpers:
    is_jwt = is_jwt
    is_absent = is_absent
    is_datetime = is_datetime


def make_token(user, expired=False):
    """Creates a valid jwt for the given user"""
    from rest_framework_jwt.settings import api_settings
    from datetime import timedelta

    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    if expired:
        payload['exp'] += timedelta(days=-1)  # expire it one day ago

    token = api_settings.JWT_ENCODE_HANDLER(payload)

    return token
