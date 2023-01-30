import random
from typing import List


# from scheduler import QueueScheduler


class Layer:
    _queue_schedulers = []

    def __init__(self, queue_schedulers, schedulers_priority: List[float]):
        if not len(queue_schedulers):
            raise ValueError('schedulers must at least have one scheduler instance')
        self._queue_schedulers = queue_schedulers
        self._schedulers_priority = schedulers_priority

    @property
    def schedulers(self):
        return self._queue_schedulers

    @property
    def highest_priority_scheduler(self):
        # todo: get by highest priority
        peeked_scheduler_idx = self.highest_priority_scheduler_index
        peeked_scheduler = self._queue_schedulers[peeked_scheduler_idx]
        for scheduler in [self._queue_schedulers[(peeked_scheduler_idx + j) % len(self._queue_schedulers)] for j in
                          range(len(self._queue_schedulers))]:
            if len(scheduler.uncompleted_jobs):
                peeked_scheduler = scheduler
                break
        return peeked_scheduler

    @property
    def highest_priority_scheduler_index(self) -> int:
        # todo: refactor for extra point
        return random.choices(list(range(len(self.schedulers))), k=1, weights=self._schedulers_priority)[0]

    @property
    def jobs_length_in_queues(self) -> int:
        return sum(
            map(lambda scheduler: len(scheduler.uncompleted_jobs), self._queue_schedulers)
        )
