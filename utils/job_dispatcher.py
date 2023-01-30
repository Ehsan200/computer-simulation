from layer import Layer


class JobDispatcher:
    @staticmethod
    def dispatch(layer: Layer, cpu_busy_time):
        scheduler = layer.highest_priority_scheduler
        job = scheduler.dequeue_job()
        if scheduler.should_run_task(job):
            job.incr_executed_time(scheduler.name)
            if not job.is_idle:
                cpu_busy_time += 1
        else:
            scheduler.pop_job(job)
            # todo: need check index out of range?
            new_scheduler = layer.schedulers[min(layer.schedulers.index(scheduler) + 1, len(layer.schedulers) - 1)]
            new_scheduler.add_new_job(job)
        return cpu_busy_time
