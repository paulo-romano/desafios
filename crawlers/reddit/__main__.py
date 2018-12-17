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
@utils.command_surrounded_by_frame
@utils.command_exception_handler
@utils.command_logging
def get_reddits(subreddits, log):
    pprint(utils.get_reddits(subreddits), indent=2)


if __name__ == '__main__':
    get_reddits()
