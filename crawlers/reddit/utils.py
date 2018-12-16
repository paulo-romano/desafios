def command_surrounded_by_frame(func):
    """Surround given function execution with a frame.

    :param func: Original function
    :return: new callable
    :rtype: callable
    """
    def inner(*args, **kwargs):
        max_length = 80
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


def _split_subreddit_names(subreddit_names):
    """Split subreddit names into a tuple.

    :param subreddit_names: Name of subbreddits separated by ";".
    :type subreddit_names: str
    :return: Tuple with subreddit names.
    :rtype: tuple
    """
    return tuple(name for name in subreddit_names.split(';') if name)
