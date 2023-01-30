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
        print(self.highest_priority_scheduler_index)
        peeked_scheduler = self.highest_priority_scheduler_index
        while peeked_scheduler < len(self._queue_schedulers) - 1:
            if not len(self._queue_schedulers[peeked_scheduler].uncompleted_jobs):
                peeked_scheduler += 1
        return self._queue_schedulers[self.highest_priority_scheduler_index]

    @property
    def highest_priority_scheduler_index(self) -> int:
        # todo: refactor for extra point
        return random.choices(list(range(len(self.schedulers))), k=1, weights=self._schedulers_priority)[0]

    @property
    def jobs_length_in_queues(self) -> int:
        return sum(
            map(lambda scheduler: len(scheduler.all_jobs), self._queue_schedulers)
        )
