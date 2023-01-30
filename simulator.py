from typing import Tuple, List

from job import Job
from layer import Layer
from utils.job_loader import JobLoader
from utils.job_creator import JobCreator
from utils.job_dispatcher import JobDispatcher


class Simulator:
    _layers = Tuple[Layer, Layer]
    _current_time: int
    _check_duration_time: int
    _check_job_count: int
    _simulation_time: int
    _total_jobs_count: int

    def __init__(
            self,
            layers: Tuple[Layer, Layer],
            check_duration_time: int,
            check_job_count: int,
            simulation_time: int,
            total_jobs_count: int
    ):
        self._layers = layers
        self._current_time = 0
        self._check_duration_time = check_duration_time
        self._check_job_count = check_job_count
        self._simulation_time = simulation_time
        self._total_jobs_count = total_jobs_count

    @property
    def _should_load_jobs(self):
        return self._current_time % self._check_duration_time == 0 and \
            self._layers[1].jobs_length_in_queues < self._check_job_count

    def _add_jobs_to_layer_one(self, jobs: List[Job]):
        for job in jobs:
            self._layers[0].schedulers[0].add_new_job(job)

    def simulate(self):
        all_jobs = JobCreator.create(n=self._total_jobs_count)
        self._add_jobs_to_layer_one(all_jobs)
        while self._current_time < self._simulation_time:

            if self._should_load_jobs:
                JobLoader.load(
                    scheduler=self._layers[1].highest_priority_scheduler,
                    previous_scheduler=self._layers[0].schedulers[0],
                    k=self._check_job_count,
                )

            JobDispatcher.dispatch(layer=self._layers[1])

            self._current_time += 1
            print(f'current time -> {self._current_time}')

        # todo: add logs ...
        print('simulation done!')
