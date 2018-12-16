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
    def _get_request_reddit_function():
        return getattr(utils, '_request_reddit')

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

        _request_reddit = self._get_request_reddit_function()
        _request_reddit(subreddit_name)

        assert mocked_request_get.called is True
        assert mocker.call(url, headers=utils.HEADERS) in \
            mocked_request_get.call_args_list

    def test_must_raise_error(self, mocker):
        subreddit_name = 'cats'

        mocked_request_get = \
            mocker.patch('requests.get', side_effect=requests.Timeout)

        _request_reddit = self._get_request_reddit_function()

        with pytest.raises(Exception) as ex:
            _request_reddit(subreddit_name)

        assert mocked_request_get.called is True
        assert ex.value.args[0] == f'Can not request "{subreddit_name}".'


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


class TestGetReddits:
    def test_must_split_subreddit_names(self, mocker):
        _split_subreddit_names = \
            mocker.patch('reddit.utils._split_subreddit_names')
        subreddit_names = 'cats;bear'
        utils.get_reddits(subreddit_names)
        assert _split_subreddit_names.called is True
        assert mocker.call(subreddit_names) in \
            _split_subreddit_names.call_args_list
