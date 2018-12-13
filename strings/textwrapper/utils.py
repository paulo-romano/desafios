import textwrap


def _wrap_text(text, max_length):
    """ Wrap given text, splinting it into line with limited length.

    :param text: Text to be wrapped
    :type text: str
    :param max_length:
    :type max_length: int
    :return: Text splitted into lines
    :rtype: list
    """
    return textwrap.wrap(text, max_length)
