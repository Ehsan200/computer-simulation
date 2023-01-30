from typing import List
import random
import numpy as np
from job import Job


class Priority:
    HIGH = 3
    NORMAL = 2
    LOW = 1


class JobCreator:
    @staticmethod
    def create(n, z, x, y) -> List[Job]:
        jobs = [Job(
            priority=random.choices([Priority.LOW, Priority.NORMAL, Priority.HIGH], weights=(7, 2, 1), k=1)[0],
            duration=np.random.exponential(scale=y, size=1)[0],
            timeout=np.random.exponential(scale=z, size=1)[0],
            arrival_time=0
        )]
        last_arrive = 0
        for _ in range(n - 1):
            last_arrive = last_arrive + int(np.random.exponential(scale=1 / x, size=1)[0])
            jobs.append(Job(
                priority=random.choices([Priority.LOW, Priority.NORMAL, Priority.HIGH], weights=(7, 2, 1), k=1)[0],
                duration=int(np.random.exponential(scale=y, size=1)[0]),
                timeout=int(np.random.exponential(scale=z, size=1)[0]),
                arrival_time=last_arrive
            ))

        return jobs
