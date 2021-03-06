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
@click.option('--max-length', default=40, help='Max line column length.')
@click.option('--justify', '-j', default=False, multiple=True,
              is_flag=True, help='Justify text')
@utils.command_surrounded_by_frame
@utils.command_exception_handler
def text_wrapper(text, max_length, justify):
    print(utils.get_formatted_text(text, max_length, justify))


@command_group.command(
    name='file',
    short_help='Split file text into lines.'
)
@click.argument('file_path')
@click.option('--max-length', default=40, help='Max line column length.')
@click.option('--justify', '-j', default=False, multiple=True,
              is_flag=True, help='Justify text')
@utils.command_surrounded_by_frame
@utils.command_exception_handler
def file_wrapper(file_path, max_length, justify):
    print(
        utils.get_formatted_text(
            utils.read_text_from_file(file_path),
            max_length,
            justify)
    )


if __name__ == '__main__':
    command_group()
