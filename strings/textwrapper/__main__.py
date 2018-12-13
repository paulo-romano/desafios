import click

import utils


@click.command()
@click.argument('text')
@click.option('--max-length', default=40)
def textwrapper(text, max_length):
    print('=' * max_length)
    print(utils.get_formatted_text(text, max_length))
    print('=' * max_length)


if __name__ == '__main__':
    textwrapper()
