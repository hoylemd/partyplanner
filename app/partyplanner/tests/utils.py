from django.test import TestCase
from json.decoder import JSONDecodeError


def check_dict_keys(subject, model):
    """
    check that each key in `model` is reflected in `subject`

    returns a dict mapping the 'bad' keys to the reason they are 'bad', or a
        similar dict for a nested layer

    :param subject dict: The dict object to compare to `model`
    :param model dict: The 'spec' dict object to which `subject` will be
        compared
    :returns dict: mapping of bad keys to reason string or dict of nested bad
        keys
    """

    bad_keys = {}

    for k, v in model.items():
        # check for type mismatch
        if not isinstance(subject[k], model[k].__class__):
            bad_keys[k] = (
                f'wrong type: {subject[k].__class__.__name__} '
                f'(expected {model[k].__class__.__name__})'
            )
            continue

        if isinstance(model[k], dict):
            # recursively check dicts
            bad_children = check_dict_keys(subject[k], model[k])
            if bad_children:
                bad_keys[k] = bad_children
                continue

        # handle arrays?

        if subject[k] != model[k]:
            bad_keys[k] = f'{subject[k]} != {model[k]}'

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
        self, response, blob, status_code=200, msg_prefix=""
    ):
        """
        Assert that the json body of `response` matches the spec given by
        `blob`, and that it's status code is correct.

        keys absent from `blob` will be ignored. This allows for partial
        matching.  works recursively too. If a dict is encountered at a spec'd
        key, the same checks will be done at that nested level too.

        Attempts to compose a highly readable error report too

        :param response : The test client response to test
        :param blob dict: spec for the body to test against
        :param status_code int: expected HTTP status code
        :param msg_prefix str: Message with which to prefix the error
            default: 'JSON Mismatch'
        :returns: a dict mapping erroneous field keys to a reason string or a
            similar dict for nested layers
        :raises AssertionError: if the status code is wrong or some keys are
            mismatched
        """

        if response.status_code != status_code:
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

        bad_keys = check_dict_keys(content, blob)
        if bad_keys:
            msg = (
                f"{(msg_prefix + ': ') if msg_prefix else ''}"
                f"Dict does not match spec on these keys:\n" +
                '\n'.join(print_bad_keys(bad_keys))
            )
            exc = AssertionError(msg)
            exc.bad_keys = bad_keys
            raise exc
