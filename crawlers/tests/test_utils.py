import pytest

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
