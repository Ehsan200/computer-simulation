from typing import List

from job import Job
from scheduler import QueueScheduler


class JobLoader:
    @staticmethod
    def load(scheduler: QueueScheduler, jobs: List[Job], k: int):
        # todo: sort and filter, pop these k jobs from layer one queue use pop_job method
        for job in jobs[:k]:
            scheduler.add_new_job(job)
