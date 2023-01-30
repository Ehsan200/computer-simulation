import numpy as np

from layer import Layer
from scheduler import QueueScheduler
from simulator import Simulator

simulator_instance = Simulator(
    layers=(
        Layer([
            QueueScheduler(name='priority', quantum_time=np.inf),
        ], [1]),
        Layer([
            QueueScheduler(name='RR1', quantum_time=2),
            QueueScheduler(name='RR2', quantum_time=4),
            QueueScheduler(name='FIFO', quantum_time=np.inf),
        ], [0.8, 0.1, 0.1]),
    ),
    total_jobs_count=1000,
    simulation_time=10,
    check_duration_time=15,
    # k
    check_job_count=20,
)

simulator_instance.simulate()
