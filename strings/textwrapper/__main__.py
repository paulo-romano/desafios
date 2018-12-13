import click

import utils


@click.command()
@click.argument('text')
@click.option('--max-length', default=40)
def textwrapper(text, max_length):
    print('=' * max_length)
    try:
        print(utils.get_formatted_text(text, max_length))
    except Exception as ex:
        print(f'Error: {ex}')
    print('=' * max_length)


if __name__ == '__main__':
    textwrapper()
