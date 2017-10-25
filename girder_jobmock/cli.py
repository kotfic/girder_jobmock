from .jobmock import (
    execute_single_job,
    chain_three_jobs,
    group_three_jobs,
    admin_user
)

import click
import asyncio
import logging

global ioloop



@click.group()
@click.option('--verbose', '-v', count=True,
              help='Once for info,  twice for debug')
def cli(verbose):
    global ioloop
    from girder.utility.server import configureServer
    plugins = ['jobs']
    webroot, appconf = configureServer(plugins=plugins)
    ioloop = asyncio.get_event_loop()

    # Set up logging
    log = logging.getLogger('girderjobmock')
    if verbose == 1:
        log.setLevel(logging.INFO)
    elif verbose == 2:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARNING)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)


@cli.resultcallback()
def close_loop(*args, **kwargs):
    ioloop.close()


@cli.command()
def cleanup():
    log = logging.getLogger('girderjobmock')

    from girder.plugins.jobs.models.job import Job
    query = {"type": { "$in": ["jobmock"] }}
    count = Job().removeWithQuery(query).deleted_count

    log.info("Deleted {} jobs.".format(count))


@cli.command()
@click.option('--delay', '-d', type=float, default=None,
           help='How much to delay state trasitions for the Job')
def single(delay):
    ioloop.run_until_complete(execute_single_job(delay=delay))


@cli.command()
@click.option('--delay', '-d', type=float, default=None,
            help='How much to delay state trasitions for the Job')
def chain(delay):
    ioloop.run_until_complete(chain_three_jobs(delay=delay))

@cli.command()
@click.option('--delay', '-d', type=float, default=None,
            help='How much to delay state trasitions for the Job')
def group(delay):
    ioloop.run_until_complete(group_three_jobs(delay=delay))
