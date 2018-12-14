import textwrap


def _wrap_text(text, max_length):
    """Wrap given text, splinting it into line with limited length.

    :param text: Text to be wrapped
    :type text: str
    :param max_length:
    :type max_length: int
    :return: Text splitted into lines
    :rtype: list
    """
    return textwrap.wrap(text, max_length)


def _join_lines(lines):
    """Join lines into a single string

    :param lines: Lines to be joined
    :type lines: list
    :return: string
    :rtype: str
    """
    return '\n'.join(lines)


def get_formatted_text(text, max_length):
    """Return formatted text.

    :param text: Text to be wrapped
    :type text: str
    :param max_length:
    :type max_length: int
    :raise ValueError
    :return: Formatted text
    :rtype: str
    """
    if max_length < 10:
        raise ValueError('Max length can not be lower than 10.')

    return _join_lines(_wrap_text(text, max_length))


def command_surrounded_by_frame(func):
    """Surround given function execution with a frame.

    :param func: Original function
    :return: new callable
    :rtype: callable
    """
    def inner(*args, **kwargs):
        max_length = kwargs.get('max_length', 0)
        print('=' * max_length)
        func(*args, **kwargs)
        print('=' * max_length)

    return inner
