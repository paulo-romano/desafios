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
    return _join_lines(_wrap_text(text, max_length))
