import abc
from collections import defaultdict
from typing import Dict

from utils import IdGenerator


class BaseJob(abc.ABC):
    _id: str
    _executed_time: Dict[str, int]

    def __init__(self):
        self._executed_time = defaultdict(int)

    def get_executed_time_in_queue(self, queue_name: str) -> int:
        return self._executed_time[queue_name]

    def incr_executed_time(self, queue_name: str):
        self._executed_time[queue_name] += 1

    @property
    def _total_executed_time(self) -> int:
        return sum(self._executed_time.values())

    @abc.abstractmethod
    @property
    def is_idle(self) -> bool:
        ...

    @abc.abstractmethod
    @property
    def is_done(self) -> bool:
        ...


class Job(BaseJob):
    _priority: int
    _duration: int
    _waited_time: Dict[str, int]

    def __init__(self, priority: int, duration: int):
        super().__init__()
        self._id = str(IdGenerator.generate())
        self._priority = priority
        self._duration = duration
        self._waited_time = defaultdict(int)

    @property
    def _total_waited_time(self) -> int:
        return sum(self._waited_time.values())

    @property
    def is_done(self) -> bool:
        return self._total_executed_time == self._duration

    @property
    def is_idle(self) -> bool:
        return False

    def incr_waited_time(self, queue_name: str):
        self._waited_time[queue_name] += 1

    def get_waited_time_in_queue(self, queue_name: str) -> int:
        return self._waited_time[queue_name]


class IdleJob(BaseJob):
    def __init__(self):
        super().__init__()
        self._id = f'idle: {self._id}'

    @property
    def is_idle(self) -> bool:
        return True

    @property
    def is_done(self) -> bool:
        return True
