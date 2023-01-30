import numpy as np
import pandas as pd
from typing import Tuple, List
from IPython.display import display

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
    _x: float
    _y: float
    _z: float

    def __init__(
            self,
            layers: Tuple[Layer, Layer],
            check_duration_time: int,
            check_job_count: int,
            simulation_time: int,
            total_jobs_count: int,
            x,
            y,
            z
    ):
        self._layers = layers
        self._current_time = 0
        self._check_duration_time = check_duration_time
        self._check_job_count = check_job_count
        self._simulation_time = simulation_time
        self._total_jobs_count = total_jobs_count
        self.monitoring_df = pd.DataFrame({
            'time': [],
            'RR1_queue_length': [],
            'RR2_queue_length': [],
            'FCFS_queue_length': []
        })
        self.cpu_busy_time = 0
        self._x = x
        self._y = y
        self._z = z

    @property
    def _should_load_jobs(self):
        return self._current_time % self._check_duration_time == 0 and \
            self._layers[1].jobs_length_in_queues < self._check_job_count

    def _add_jobs_to_layer_one(self, jobs: List[Job]):
        for job in jobs:
            self._layers[0].schedulers[0].add_new_job(job)

    def simulate(self):
        all_jobs = JobCreator.create(n=self._total_jobs_count, z=self._z, x=self._x, y=self._y)
        self._add_jobs_to_layer_one(all_jobs)
        while self._current_time < self._simulation_time:

            if self._should_load_jobs:
                JobLoader.load(
                    scheduler=self._layers[1]._queue_schedulers[0],
                    previous_scheduler=self._layers[0].schedulers[0],
                    k=self._check_job_count,
                    current_time=self._current_time
                )

            self.cpu_busy_time = JobDispatcher.dispatch(layer=self._layers[1], cpu_busy_time=self.cpu_busy_time)

            for job in self._layers[0].schedulers[0].all_jobs:
                if job._arrival_time < self._current_time:
                    job.incr_waited_time(self._layers[0].schedulers[0].name)

            for scheduler in self._layers[1].schedulers:
                for job in scheduler.uncompleted_jobs:
                    job.incr_waited_time(scheduler.name)

            self._current_time += 1
            self.monitoring_df.loc[
                len(self.monitoring_df.index)] = [self._current_time,
                                                  len(self._layers[1].schedulers[0].uncompleted_jobs),
                                                  len(self._layers[1].schedulers[1].uncompleted_jobs),
                                                  len(self._layers[1].schedulers[2].uncompleted_jobs)]

            # todo: add logs ...
        print('simulation done!')
        self.monitoring_df.to_csv('report.csv')
        print(f'cpu utilization: {self.cpu_busy_time / self._simulation_time}')
        print(f'average RR1 queue length: ', self.monitoring_df.loc[:, 'RR1_queue_length'].mean())
        print(f'average RR2 queue length: ', self.monitoring_df.loc[:, 'RR2_queue_length'].mean())
        print(f'average FCFS queue length: ', self.monitoring_df.loc[:, 'FCFS_queue_length'].mean())
        print('average RR1 wait time: ',
              round(np.mean([j._waited_time['RR1'] for j in all_jobs]), 2))
        print('average RR2 wait time: ',
              round(np.mean([j._waited_time['RR2'] for j in all_jobs]), 2))
        print('average FCFS wait time: ',
              round(np.mean([j._waited_time['FCFS'] for j in all_jobs]), 2))
        print(f'expired jobs percentage:  %{len([j for j in all_jobs if j._is_expired]) / self._total_jobs_count}')
