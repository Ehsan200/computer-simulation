from typing import List
import random

from job import Job


class Priority:
    HIGH = 1
    NORMAL = 2
    LOW = 3


class JobCreator:
    @staticmethod
    def create(n) -> List[Job]:
        # todo: create jobs in proper way
        return [
            Job(
                priority=random.choices([Priority.LOW, Priority.NORMAL, Priority.HIGH], weights=(7, 2, 1), k=1)[0],
                duration=random.choices([1, 2, 3, 4, 5, 6, 7, 8], k=1)[0]
            ) for _ in range(n)
        ]
