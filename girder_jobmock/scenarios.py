from .jobmock import execute, job, group
import random

async def execute_single_job(finish_delay=None, error=False):
    from girder.plugins.jobs.constants import JobStatus
    start_delay=None
    trans = [(JobStatus.RUNNING, start_delay), (JobStatus.SUCCESS, finish_delay)] if error else \
            [(JobStatus.RUNNING, start_delay), (JobStatus.ERROR, finish_delay)]
    await execute(
        job('Single Job', trans),
    )


async def chain_N_jobs(N, finish_delay=None, error=None):
    from girder.plugins.jobs.constants import JobStatus
    start_delay=None
    error_trans = [(JobStatus.RUNNING, start_delay),
                   (JobStatus.ERROR, finish_delay)]

    success_trans = [(JobStatus.RUNNING, start_delay),
                     (JobStatus.SUCCESS, finish_delay)]

    jobs = []
    for i in range(N):
        if i == error:
            jobs.append(job('Chain {}'.format(i), error_trans))
            break
        else:
            jobs.append(job('Chain {}'.format(i), success_trans))

    await execute(*jobs)


async def group_N_jobs(N, finish_delay=None, error_rate=0):
    from girder.plugins.jobs.constants import JobStatus
    start_delay=None
    error_trans = [(JobStatus.RUNNING, start_delay),
                   (JobStatus.ERROR, finish_delay)]

    success_trans = [(JobStatus.RUNNING, start_delay),
                     (JobStatus.SUCCESS, finish_delay)]

    await execute(
        group(*[job("Group {}".format(i),
                    random.choices([error_trans, success_trans],
                                   (error_rate, 1.0 - error_rate))[0])
                for i in range(N)])
    )


async def chord_N_jobs(N, finish_delay=None, error_rate=0):
    from girder.plugins.jobs.constants import JobStatus
    start_delay=None
    error_trans = [(JobStatus.RUNNING, start_delay),
                   (JobStatus.ERROR, finish_delay)]

    success_trans = [(JobStatus.RUNNING, start_delay),
                     (JobStatus.SUCCESS, finish_delay)]

    await execute(
        group(*[job("Map {}".format(i),
                    random.choices([error_trans, success_trans],
                                   (error_rate, 1.0 - error_rate))[0])
                for i in range(N)]),
        job('Reduce 0', success_trans)
    )



async def basic_workflow(finish_delay=None):
    from girder.plugins.jobs.constants import JobStatus
    start_delay=None
    success_trans = [(JobStatus.RUNNING, start_delay),
                     (JobStatus.SUCCESS, finish_delay)]

    await execute(
        job('Root', success_trans),
        job('Chain 1', success_trans),
        group(
            job('Map 0', success_trans),
            job('Map 1', success_trans),
            job('Map 2', success_trans)),
        job('Reduce 0', success_trans)
    )
