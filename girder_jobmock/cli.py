from . import FloatRange, distribution
from .jobmock import admin_user
from .scenarios import (
    execute_single_job,
    chain_N_jobs,
    group_N_jobs,
    chord_N_jobs,
    basic_workflow)

import click
import asyncio
import logging
import sys

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
@click.option('--delay', '-d', multiple=True, type=float, callback=distribution,
            help='How much to delay finish trasition for the Job')
@click.option('--error', '-e', is_flag=True,
              help='Transition to Error instead of Success')
def single(delay, error):
    ioloop.run_until_complete(
        execute_single_job(delay, not error))


@cli.command()
@click.option('--number', '-n', type=int, default=3,
            help='How many jobs to generate')
@click.option('--delay', '-d', multiple=True, type=float, callback=distribution,
            help='How much to delay finish trasition for the Job')
@click.option('--error', '-e', type=int, default=-1,
              help='Zero-indexed job to error out on (No error by default)')
def chain(number, delay, error):
    ioloop.run_until_complete(
        chain_N_jobs(number, delay, error))

@cli.command()
@click.option('--number', '-n', type=int, default=3,
            help='How many jobs to generate')
@click.option('--delay', '-d', multiple=True, type=float, callback=distribution,
            help='How much to delay finish trasition for the Job')
@click.option('--error', '-e', type=FloatRange(0.0, 1.0), default=0.0,
            help='Rough percentage of jobs that error')
def chord(number, delay, error):
    ioloop.run_until_complete(
        chord_N_jobs(number, delay, error))


@cli.command()
@click.option('--number', '-n', type=int, default=3,
            help='How many jobs to generate')
@click.option('--delay', '-d', multiple=True, type=float, callback=distribution,
            help='How much to delay finish trasition for the Job')
@click.option('--error', '-e', type=FloatRange(0.0, 1.0), default=0.0,
            help='Rough percentage of jobs that error')
def group(number, delay, error):
    ioloop.run_until_complete(
        group_N_jobs(number, delay, error))


@cli.command()
@click.option('--delay', '-d', multiple=True, type=float, callback=distribution,
            help='How much to delay finish trasition for the Job')
def workflow(delay):
    ioloop.run_until_complete(basic_workflow(finish_delay=delay))


@cli.command(help='View a histogram of the timing distribution')
@click.option('--dist', '-d', multiple=True, type=float, callback=distribution)
def dist(dist):
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError:
        log = logging.getLogger('girderjobmock')
        log.error("Please install matplotlib and seaborn!")
        sys.exit(1)

    ax = sns.distplot([dist() for _ in range(5000)])
    ax.set(xlabel='Seconds')
    plt.show()
