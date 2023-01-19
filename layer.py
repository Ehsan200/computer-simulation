from typing import List

from scheduler import QueueScheduler


class Layer:
    _queue_schedulers = List[QueueScheduler]

    def __init__(self, queue_schedulers: List[QueueScheduler]):
        if not len(queue_schedulers):
            raise ValueError('schedulers must at least have one scheduler instance')
        self._queue_schedulers = queue_schedulers

    @property
    def schedulers(self) -> List[QueueScheduler]:
        return self._queue_schedulers

    @property
    def highest_priority_scheduler(self) -> QueueScheduler:
        # todo: get by highest priority
        return self._queue_schedulers[self.highest_priority_scheduler_index]

    @property
    def highest_priority_scheduler_index(self) -> int:
        # todo: refactor for extra point
        return 0

    @property
    def jobs_length_in_queues(self) -> int:
        return sum(
            map(lambda scheduler: len(scheduler.all_jobs), self._queue_schedulers)
        )
