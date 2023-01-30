from typing import List

from job import Job
from scheduler import QueueScheduler


class JobLoader:
    @staticmethod
    def load(scheduler: QueueScheduler, previous_scheduler: QueueScheduler, k: int, current_time):
        jobs = [job for job in previous_scheduler.all_jobs if job._arrival_time <= current_time]
        sorted_jobs = sorted(jobs, key=lambda job: (job._priority, job._total_waited_time), reverse=True)
        # todo: sort and filter, pop these k jobs from layer one queue use pop_job method
        for job in sorted_jobs[:k]:
            previous_scheduler.pop_job(job)
            scheduler.add_new_job(job)
