import pytest
from textwrapper import utils


class TestWrapText:
    @staticmethod
    def _get_wrap_text_function():
        return getattr(utils, '_wrap_text')

    def test_must_use_std_textwrap_wrap(self, mocker):
        mocked_std_wrap = \
            mocker.patch('textwrap.wrap', return_value='fake_text')
        _wrap_text = self._get_wrap_text_function()
        _wrap_text('ugly text', 40)
        assert mocked_std_wrap.called is True

    @pytest.mark.parametrize('text, expected_lines', (
        (
            'In the beginning God created the heavens and the earth.',
            [
                'In the beginning God created the heavens',
                'and the earth.'
            ]
        ),
        (
            'And God said, "Let there be light," and there was light. '
            'God saw that the light was good, and he separated the light '
            'from the darkness.',
            [
                'And God said, "Let there be light," and',
                'there was light. God saw that the light',
                'was good, and he separated the light',
                'from the darkness.',
            ]
        ),

    ))
    def test_must_return_lines_with_wrapped_text(self, text, expected_lines):
        _wrap_text = self._get_wrap_text_function()
        lines = _wrap_text(text, 40)
        assert lines == expected_lines

    @pytest.mark.parametrize('text, max_length, expected_lines', (
        ('And God said', 10, ['And God', 'said']),
        ('But only the Devil was listening', 20,
         ['But only the Devil', 'was listening']),
    ))
    def test_must_return_lines_with_wrapped_text_max_length(
            self, text, max_length, expected_lines):
        _wrap_text = self._get_wrap_text_function()
        lines = _wrap_text(text, max_length)
        assert lines == expected_lines


class TestJoinLines:
    @staticmethod
    def _get_join_lines_function():
        return getattr(utils, '_join_lines')

    @pytest.mark.parametrize('lines, expected_text', (
        (['super loo', 'boobaloo no'], 'super loo\nboobaloo no'),
        (
            ['God and Devil', 'False or Not', 'Who knows'],
            'God and Devil\nFalse or Not\nWho knows'
        ),
    ))
    def test_must_join_lines_with_new_line_char(
            self, lines, expected_text):
        _join_lines = self._get_join_lines_function()
        assert _join_lines(lines) == expected_text


class TestGetFormattedText:
    def test_must_return_formatted_text(self):
        raw_text = \
            'And God said, "Let there be light," and there was light. ' \
            'God saw that the light was good, and he separated the light ' \
            'from the darkness.'

        expected_text = 'And God said, "Let there be light," and\n' \
                        'there was light. God saw that the light\n' \
                        'was good, and he separated the light\n' \
                        'from the darkness.'

        assert utils.get_formatted_text(raw_text, 40) == expected_text

    def test_must_raise_error_if_length_lower_10(self):
        with pytest.raises(ValueError) as ex:
            utils.get_formatted_text('ugly text', 9)

        assert ex.value.args[0] == \
            'Max length can not be lower than 10.'


class TestCommandSurroundedByFrame:
    @pytest.mark.parametrize('max_length', (
        10, 20, 30
    ))
    def test_must_print_frame_using_max_length_value(
            self, mocker, max_length):
        @utils.command_surrounded_by_frame
        def decorated_func(text, max_length=40):
            pass

        mocked_print = mocker.patch('builtins.print')
        decorated_func('ugly text', max_length=max_length)
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

        decorated_func('ugly text', 10)

        assert mocked_print.called is True
        assert mocker.call(expected_message) in \
            mocked_print.call_args_list
