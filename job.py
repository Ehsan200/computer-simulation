import abc
import math
from collections import defaultdict
from typing import Dict

from utils.id_generator import IdGenerator


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

    @property
    @abc.abstractmethod
    def is_idle(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def is_done(self) -> bool:
        ...


class Job(BaseJob):
    _priority: int
    _duration: int
    _waited_time: Dict[str, int]
    _timeout: int

    def __init__(self, priority: int, duration: int, timeout: int = math.inf):
        super().__init__()
        self._id = str(IdGenerator.generate())
        self._priority = priority
        self._duration = duration
        self._waited_time = defaultdict(int)
        self._timeout = timeout

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

    @property
    def timeout(self):
        return self._timeout


class IdleJob(BaseJob):
    def __init__(self):
        super().__init__()
        self._id = f'idle'

    @property
    def is_idle(self) -> bool:
        return True

    @property
    def is_done(self) -> bool:
        return True
