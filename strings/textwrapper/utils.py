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


def _fill_with_spaces(words, remaining_spaces):
    if not remaining_spaces:
        return words

    for index in range(1, len(words)):
        words[index] = words[index].rjust(len(words[index]) + 1)
        remaining_spaces -= 1

        if not remaining_spaces:
            break

    return _fill_with_spaces(words, remaining_spaces)


def justify(text, max_length):
    """Add full justify to given text.

    :param text: Text to be justified
    :type text: str
    :param max_length: Max length of line
    :type max_length: int
    :return: Justified text
    :rtype: str
    """
    text_length = len(text)

    if text_length == max_length:
        return text

    words = text.split(' ')

    if len(words) == 2:
        remaining_spaces = max_length - text_length
        return f'{words[0]}{" " * remaining_spaces}{words[1]}'

    remaining_spaces = (max_length - text_length)

    words = _fill_with_spaces(words, remaining_spaces)

    return ' '.join(words)


def _justifier(max_length, justify_text):
    """Return a preconfigured justify function.

    :param max_length: Max length of line
    :type max_length: int
    :param justify_text: If true text will be full justified.
    :type justify_text: bool
    :return: Preconfigured justify function.
    :rtype: callable
    """
    def inner(text):
        return justify(text, max_length) \
            if justify_text else text

    return inner


def get_formatted_text(text, max_length, justify_text=False):
    """Return formatted text.

    :param text: Text to be wrapped
    :type text: str
    :param max_length: Max length of line
    :type max_length: int
    :param justify_text: If true text will be full justified.
    :type justify_text: bool
    :raise ValueError
    :return: Formatted text
    :rtype: str
    """
    if max_length < 10:
        raise ValueError('Max length can not be lower than 10.')

    lines = _wrap_text(text, max_length)

    lines = map(_justifier(max_length, justify_text), lines)

    return _join_lines(lines)


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


def command_exception_handler(func):
    """Handle with command execution errors

    :param func: Original function
    :return: new callable
    :rtype: callable
    """
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            message = ex if any(ex.args) else type(ex).__name__
            print(f'Error: {message}')

    return inner


def read_text_from_file(file_path):
    """Read content from file.

    :param file_path: File path
    :type file_path: str
    :raises Exception
    :return: File content
    :rtype: str
    """
    try:
        with open(file_path) as file:
            text = file.read()
        return text
    except Exception:
        raise Exception(
            f'Can not read "{file_path}" file.'
        ) from None
