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
