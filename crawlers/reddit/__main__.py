from pprint import pprint

import click

import utils


@click.command(name='reddit')
@click.argument('subreddits')
@utils.command_surrounded_by_frame
@utils.command_exception_handler
def get_reddits(subreddits):
    pprint(utils.get_reddits(subreddits), indent=2)


if __name__ == '__main__':
    get_reddits()
