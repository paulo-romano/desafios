from pprint import pprint

import click

import utils


@click.command(name='reddit')
@click.argument('subreddits')
@click.option(
    '--log', '-l',
    default=False,
    multiple=True,
    is_flag=True,
    help='Activate logging.',
)
@click.option(
    '--min-upvotes',
    default=5000,
    help='Min up votes value.',
)
@utils.command_surrounded_by_frame
@utils.command_exception_handler
@utils.command_logging
def get_reddits(subreddits, log, min_upvotes):
    pprint(utils.get_reddits(subreddits, min_upvotes), indent=2)


if __name__ == '__main__':
    get_reddits()
