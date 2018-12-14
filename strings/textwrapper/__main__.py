import click

import utils


@click.group()
def command_group():
    pass


@command_group.command(
    name='text',
    short_help='Split text into lines.'
)
@click.argument('text')
@click.option('--max-length', default=40)
@utils.command_surrounded_by_frame
@utils.command_exception_handler
def textwrapper(text, max_length):
    print(utils.get_formatted_text(text, max_length))


if __name__ == '__main__':
    command_group()
