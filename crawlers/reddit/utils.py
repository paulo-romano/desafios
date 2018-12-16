BASE_URL = 'https://old.reddit.com'
BASE_URL_SUBREDDIT = '/r/{subreddit}/top/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'
}


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


def _request_reddit(subreddit_name):
    import requests
    try:
        url = f'{BASE_URL}{BASE_URL_SUBREDDIT}'
        return requests.get(
            url.format(subreddit=subreddit_name),
            headers=HEADERS,
        )
    except Exception:
        raise Exception(f'Can not request "{subreddit_name}".') from None


def _parse_reddit_items(soup):
    threads = soup.find_all('div', {'class': 'thing'})

    items = []
    for thread in threads:

        items.append({
            'title': thread.find('a', {'class': 'title'}).text,
            'link': thread.get('data-url'),
            'upvotes': thread.get('data-score'),
            'comments_link': f'{BASE_URL}{thread.get("data-permalink")}',
            'subreddit_link': f'{BASE_URL}/r/{thread.get("data-subreddit")}',
        })

    return items


def _parse_response(response):
    from bs4 import BeautifulSoup
    try:
        return _parse_reddit_items(
            BeautifulSoup(response.content, 'html.parser')
        )

    except Exception:
        raise Exception(f'Can not parse response.') from None


def get_reddits(subreddit_names):
    subreddits = _split_subreddit_names(subreddit_names)

    response = map(_request_reddit, subreddits)
    response = map(_parse_response, response)

    return list(response)
