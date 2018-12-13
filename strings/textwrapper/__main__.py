import click


@click.command()
@click.argument('text')
def textwrapper(text):
    print(text)


if __name__ == '__main__':
    textwrapper()
