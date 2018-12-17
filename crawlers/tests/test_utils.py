import pytest
import requests
from bs4 import BeautifulSoup

from reddit import utils


class TestCommandSurroundedByFrame:
    def test_must_print_frame_using_max_length_value(
            self, mocker):
        @utils.command_surrounded_by_frame
        def decorated_func(_):
            pass

        max_length = 80
        mocked_print = mocker.patch('builtins.print')
        decorated_func('cats;dogs')
        assert mocked_print.called is True
        assert mocked_print.call_count == 2
        assert mocked_print.call_args_list[0] == \
            mocker.call('=' * max_length)
        assert mocked_print.call_args_list[1] == \
            mocker.call('=' * max_length)


class TestCommandExceptionHandler:
    @pytest.mark.parametrize('exception, expected_message', (
        (Exception('error123'), 'Error: error123'),
        (Exception(), 'Error: Exception'),
    ))
    def test_must_print_exception(
            self, mocker, exception, expected_message):
        @utils.command_exception_handler
        def decorated_func(text, max_length=40):
            raise exception

        mocked_print = mocker.patch('builtins.print')

        decorated_func('cat;dogs', 10)

        assert mocked_print.called is True
        assert mocker.call(expected_message) in \
            mocked_print.call_args_list


class TestSplitSubRedditNames:
    @staticmethod
    def _get_split_subreddit_names_function():
        return getattr(utils, '_split_subreddit_names')

    @pytest.mark.parametrize('subreddit_names, expected_values', (
        ('cats', ('cats',)),
        ('cats;', ('cats',)),
        (';cats', ('cats',)),
        (';cats;', ('cats',)),
        ('cats;dogs', ('cats', 'dogs')),
        ('cats;dogs;cows', ('cats', 'dogs', 'cows')),
    ))
    def test_must_split(self, subreddit_names, expected_values):
        _split_subreddit_names = self._get_split_subreddit_names_function()
        assert _split_subreddit_names(subreddit_names) == expected_values


class TestRequestReddit:
    @staticmethod
    def _get_request_subreddit_function():
        return getattr(utils, '_request_subreddit')

    @staticmethod
    def _get_url(subreddit_name):
        return f'{utils.BASE_URL}{utils.BASE_URL_SUBREDDIT}' \
               .format(subreddit=subreddit_name)

    def test_must_request_reddit(self, mocker):
        subreddit_name = 'cats'
        fake_response = requests.Response()
        url = self._get_url(subreddit_name)

        mocked_request_get = \
            mocker.patch('requests.get', return_value=fake_response)

        _request_reddit = self._get_request_subreddit_function()
        _request_reddit(subreddit_name)

        assert mocked_request_get.called is True
        assert mocker.call(url, headers=utils.HEADERS) in \
            mocked_request_get.call_args_list

    def test_must_raise_error(self, mocker):
        subreddit_name = 'cats'

        mocked_request_get = \
            mocker.patch('requests.get', side_effect=requests.Timeout)

        _request_reddit = self._get_request_subreddit_function()

        with pytest.raises(Exception) as ex:
            _request_reddit(subreddit_name)

        assert mocked_request_get.called is True
        assert ex.value.args[0] == f'Can not request "https://old.reddit' \
                                   f'.com/r/{subreddit_name}/top/".'


class TestParseResponse:
    @staticmethod
    def _get_parse_response_function():
        return getattr(utils, '_parse_response')

    def test_must_raise_error(self, mocker):
        fake_response = requests.Response()
        setattr(fake_response, '_content', 'fake_content')

        __init__ = mocker.patch.object(
            BeautifulSoup, '__init__', side_effect=Exception)

        _parse_response = self._get_parse_response_function()

        with pytest.raises(Exception) as ex:
            _parse_response(fake_response)

        assert __init__.called is True
        assert mocker.call(fake_response.content, 'html.parser') in \
            __init__.call_args_list
        assert ex.value.args[0] == 'Can not parse response.'

    def test_must_call_parse_reddit_items(self, mocker):
        fake_response = requests.Response()
        setattr(fake_response, '_content', 'fake_content')

        fake_items = 'fake_items'

        __new__ = mocker.patch.object(
            BeautifulSoup, '__new__',
            return_value=BeautifulSoup('', 'html.parser'))

        _parse_reddit_items = mocker.patch(
            'reddit.utils._parse_reddit_items',
            return_value=fake_items
        )

        _parse_response = self._get_parse_response_function()
        assert _parse_response(fake_response) == fake_items

        assert __new__.called is True
        assert _parse_reddit_items.called is True


class TestRequestConcurrent:
    @staticmethod
    def _get_request_concurrent_function():
        return getattr(utils, '_request_concurrent')

    def test_must_set_a_new_loop(self, mocker):
        mocked_new_event_loop = mocker.patch('asyncio.new_event_loop')
        mocked_set_event_loop = mocker.patch('asyncio.set_event_loop')

        _request_concurrent = self._get_request_concurrent_function()
        _request_concurrent('car')

        assert mocked_new_event_loop.called is True
        assert mocked_set_event_loop.called is True


class TestGetReddits:
    fake_response = requests.Response()
    subreddit_names = 'cats;bear'
    subreddits = 'car', 'bear'
    expected_value = 'expected_fake_value'

    def _mock_split_subreddit_names(self, mocker):
        return mocker.patch('reddit.utils._split_subreddit_names',
                            return_value=self.subreddits)

    def _mock_request_concurrent(self, mocker):
        return mocker.patch('reddit.utils._request_concurrent',
                            return_value=[self.fake_response])

    def _mock_request_concurrent_next_pages(self, mocker):
        return mocker.patch('reddit.utils._request_concurrent_next_pages',
                            return_value=[self.fake_response])

    def _mock_parse_response(self, mocker):
        return mocker.patch('reddit.utils._parse_response',
                            return_value=self.expected_value)

    def test_must_return_expected_value(self, mocker):
        self._mock_parse_response(mocker)
        self._mock_request_concurrent(mocker)
        self._mock_request_concurrent_next_pages(mocker)
        self._mock_split_subreddit_names(mocker)

        assert utils.get_reddits(self.subreddit_names)[0] == \
            self.expected_value

    def test_must_split_subreddit_names(self, mocker):
        self._mock_parse_response(mocker)
        self._mock_request_concurrent(mocker)
        self._mock_request_concurrent_next_pages(mocker)

        _split_subreddit_names = self._mock_split_subreddit_names(mocker)

        utils.get_reddits(self.subreddit_names)

        assert _split_subreddit_names.called is True

        assert mocker.call(self.subreddit_names) in \
            _split_subreddit_names.call_args_list

    def test_must_request_concurrently(self, mocker):
        self._mock_parse_response(mocker)
        self._mock_split_subreddit_names(mocker)
        self._mock_request_concurrent_next_pages(mocker)

        _request_concurrent = self._mock_request_concurrent(mocker)

        utils.get_reddits(self.subreddit_names)

        assert _request_concurrent.called is True
        assert mocker.call(self.subreddits) in \
            _request_concurrent.call_args_list

    def test_must_request__next_page_concurrently(self, mocker):
        self._mock_parse_response(mocker)
        self._mock_split_subreddit_names(mocker)
        self._mock_request_concurrent(mocker)

        _request_concurrent_next_page = \
            self._mock_request_concurrent_next_pages(mocker)

        utils.get_reddits(self.subreddit_names)

        assert _request_concurrent_next_page.called is True

    def test_must_parse_response(self, mocker):
        self._mock_request_concurrent(mocker)
        self._mock_split_subreddit_names(mocker)
        self._mock_request_concurrent_next_pages(mocker)

        _parse_response = self._mock_parse_response(mocker)

        utils.get_reddits(self.subreddit_names)

        assert _parse_response.called is True
        assert mocker.call(self.fake_response) in \
            _parse_response.call_args_list
