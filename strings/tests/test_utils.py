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
