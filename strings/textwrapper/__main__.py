import click

import utils


@click.command()
@click.argument('text')
def textwrapper(text):
    print(utils.get_formatted_text(text, 40))


if __name__ == '__main__':
    textwrapper()
