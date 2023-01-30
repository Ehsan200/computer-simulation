from typing import List

from job import BaseJob, IdleJob


class QueueScheduler:
    _jobs: List[BaseJob]
    _name: str
    _quantum_time: int

    def __init__(self, name, quantum_time):
        self._name = name
        self._jobs = []
        self._quantum_time = quantum_time

    @property
    def name(self) -> str:
        return self._name

    def should_run_task(self, job: BaseJob) -> bool:
        return job.is_idle or job.get_executed_time_in_queue(self.name) < self._quantum_time

    @property
    def all_jobs(self):
        return self._jobs

    @property
    def completed_jobs(self):
        return [_ for _ in self.all_jobs if _.is_done]

    @property
    def uncompleted_jobs(self):
        return [_ for _ in self.all_jobs if not _.is_done]

    def add_new_job(self, job: BaseJob):
        self._jobs.append(job)

    def dequeue_job(self) -> BaseJob:
        while True:
            if not len(self.uncompleted_jobs):
                return IdleJob()
            job = self.uncompleted_jobs[0]
            if job._total_waited_time < job.timeout:
                return job
            else:
                self.pop_job(job)

    def pop_job(self, job):
        index = self.all_jobs.index(job)
        self._jobs.pop(index)
