from typing import List

from job import Job
from scheduler import QueueScheduler


class JobLoader:
    @staticmethod
    def load(scheduler: QueueScheduler, previous_scheduler: QueueScheduler, k: int):
        jobs = previous_scheduler.all_jobs
        sorted_jobs = sorted(jobs, key=lambda job: (job._priority, job._waited_time))
        # todo: sort and filter, pop these k jobs from layer one queue use pop_job method
        for job in sorted_jobs[:k]:
            previous_scheduler.pop_job(job)
            scheduler.add_new_job(job)
