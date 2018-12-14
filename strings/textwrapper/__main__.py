import click

import utils


@click.command()
@click.argument('text')
@click.option('--max-length', default=40)
@utils.command_surrounded_by_frame
def textwrapper(text, max_length):
    try:
        print(utils.get_formatted_text(text, max_length))
    except Exception as ex:
        print(f'Error: {ex}')


if __name__ == '__main__':
    textwrapper()
