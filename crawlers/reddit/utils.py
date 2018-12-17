import asyncio
import concurrent
import logging
import sys

from bs4 import BeautifulSoup

BASE_URL = 'https://old.reddit.com'
BASE_URL_SUBREDDIT = '/r/{subreddit}/top/'
MAX_PAGES = 5

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


def command_logging(func):
    """Activate command logging

    :param func: Original function
    :return: new callable
    :rtype: callable
    """
    def inner(*args, **kwargs):
        if kwargs.get('log'):
            reddit = logging.getLogger()
            reddit.setLevel(logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = \
                logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            handler.setFormatter(formatter)
            reddit.addHandler(handler)
        func(*args, **kwargs)

    return inner


def _split_subreddit_names(subreddit_names):
    """Split subreddit names into a tuple.

    :param subreddit_names: Name of subbreddits separated by ";".
    :type subreddit_names: str
    :return: Tuple with subreddit names.
    :rtype: tuple
    """
    return tuple(name for name in subreddit_names.split(';') if name)


def _request_url(url):
    import requests
    try:
        return requests.get(
            url,
            headers=HEADERS,
        )
    except Exception as ex:
        logging.error(f'Can not request. {ex}')
        raise Exception(f'Can not request "{url}".') from None


def _request_subreddit(subreddit_name):
    url = f'{BASE_URL}{BASE_URL_SUBREDDIT}' \
          .format(subreddit=subreddit_name)
    return _request_url(url)


def _parse_reddit_items(soup):
    threads = soup.find_all('div', {'class': 'thing'})

    items = []
    for thread in threads:
        link = f'{BASE_URL}{thread.get("data-url")}' \
            if thread.get("data-url").startswith('/r/') \
            else thread.get("data-url")

        tittle = thread.find('a', {'class': 'title'}).text

        logging.info(f'Found thread "{tittle}"')

        items.append({
            'title': tittle,
            'link': link,
            'upvotes': thread.get('data-score'),
            'comments_link': f'{BASE_URL}{thread.get("data-permalink")}',
            'subreddit_link': f'{BASE_URL}/r/{thread.get("data-subreddit")}',
        })

    return items


def _parse_response(response):
    try:
        return _parse_reddit_items(
            BeautifulSoup(response.content, 'html.parser')
        )

    except Exception as ex:
        logging.error(f'Can not parse response. {ex}')
        raise Exception(f'Can not parse response.') from None


def _execute_func_concurrent(request_function, params):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            futures = [
                loop.run_in_executor(pool, request_function, param)
                for param in params
            ]

        loop.run_until_complete(asyncio.wait(futures))
        loop.close()

        return [future.result() for future in futures]
    except Exception as ex:
        logging.error(f'Can not execute requests as futures. {ex}')
        return []


def _request_concurrent(subreddits):
    """Request each subreddit concurrently.

    :param subreddits: Tuple of subreddits.
    :type subreddits: tuple
    :return: List of request.Response.
    :rtype: list
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    return _execute_func_concurrent(_request_subreddit, subreddits)


def _get_next_page_url(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        next_button = soup.find('span', {'class': 'next-button'})
        return next_button.find('a').get('href')
    except Exception:
        logging.error(f'There is not next button on "{response.url}".')
        return None


def _request_concurrent_next_pages(responses, current_page=0):
    """Request for response next pages concurrently.

    :param responses: List of requests.Response
    :type responses: list
    :return: List of request.Response.
    :rtype: list
    """
    if current_page == MAX_PAGES:
        return responses

    urls = [
        _get_next_page_url(response)
        for response in responses
        if _get_next_page_url(response)
    ]
    responses = _execute_func_concurrent(_request_url, urls)

    return _request_concurrent_next_pages(responses, current_page + 1)


def _unpack(parsed_responses):
    return [item for items in parsed_responses for item in items]


def get_reddits(subreddit_names):
    responses = []
    responses += _request_concurrent(_split_subreddit_names(subreddit_names))
    responses += _request_concurrent_next_pages(responses)

    parsed_responses = map(_parse_response, responses)
    parsed_responses = _unpack(parsed_responses)

    return parsed_responses
