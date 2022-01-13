from huey import crontab
from huey.contrib.djhuey import periodic_task, task

@task()
def count_beans(number):
    print('-- counted {} beans --'.format(number))
    return 'Counted {} beans'.format(number)

@periodic_task(crontab(minute='*/5'))
def every_five_mins():
    print('Every five minutes this will be printed by the consumer')