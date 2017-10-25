from girder.utility.server import configureServer
from girder.models.user import User
import time
import asyncio
import logging
import uuid
global ioloop

JOB = 1
GROUP = 2

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

admin_user =  list(User().getAdmins())[0]

def job(title, transitions, **kwargs):
    kwargs['title'] = title
    kwargs['user'] = kwargs.get('user', admin_user)
    kwargs['type'] = kwargs.get('type', 'jobmock')
    kwargs['public'] = kwargs.get('public', True)
    kwargs['otherFields'] = kwargs.get('otherFields', {})

    return JOB, (transitions,), kwargs

def group(*jobs, **kwargs):
    _group_id = uuid.uuid1()
    for job in jobs:
        job['otherFields']['groupId'] = _group_id
        job['otherFields'].update(kwargs)
    return GROUP, jobs


async def make_job(transitions, **job_kwargs):
    t0 = time.time()
    log.debug('Starting create job')
    from girder.plugins.jobs.models.job import Job

    job = Job().createJob(**job_kwargs)
    job = Job().save(job)
    log.debug('Saved job {}'.format(job['_id']))

    for state, delay in transitions:
        Job().updateJob(job, status=state)
        if delay is not None:
            await asyncio.sleep(delay)

    log.debug('Finished job {}'.format(job['_id']))
    return job['_id']

async def make_group(jobs):
    pass

async def execute(*steps):
    # Reverse the list and work from the end backwards
    steps =  list(steps)[::-1]

    _parent_id = None
    _root_id = None
    last_step = None

    while steps:
        try:
            _type, args, kwargs = steps[-1]
            if _type != JOB:
                raise ValueError()
            else:
                # Set the job's parent and root
                kwargs['otherFields']['parentId'] = _parent_id
                kwargs['otherFields']['rootId'] = _root_id
                _parent_id = await ioloop.create_task(make_job(*args, **kwargs))

        except ValueError:
            _type, jobs = steps[-1]
            if _type != GROUP:
                raise RuntimeError("Unknown type {}".format(_type))

            # Set each job's parent and root
            for _, job in jobs:
                job['otherFields']['parentId'] = _parent_id
                job['otherFields']['rootId'] = _root_id

                _parent_id = await ioloop.create_task(make_group(jobs))

        # Track the last step so we can handle parent_type correctly
        last_step = steps.pop()

        # If root is None then this is the first task and "_parent_id"
        # is also the id of the root job
        if _root_id is None:
            _root_id = _parent_id


async def execute_single_job(delay=None):
    trans = [(JobStatus.RUNNING, delay), (JobStatus.SUCCESS, delay)]
    await execute(
        job('Single Job', trans),
    )

async def chain_three_jobs(delay=None):
    trans = [(JobStatus.RUNNING, delay), (JobStatus.SUCCESS, delay)]
    await execute(
        job('Test Task 1', trans),
        job('Test Task 2', trans),
        job('Test Task 3', trans)
    )



if __name__ == '__main__':
    global ioloop
    plugins = ['jobs']
    webroot, appconf = configureServer(plugins=plugins)

    from girder.plugins.jobs.constants import JobStatus

    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(chain_three_jobs())

    ioloop.close()
