from layer import Layer


class JobDispatcher:
    @staticmethod
    def dispatch(layer: Layer):
        scheduler = layer.highest_priority_scheduler
        job = scheduler.dequeue_job()
        if scheduler.should_run_task(job):
            job.incr_executed_time(scheduler.name)
        else:
            scheduler.pop_job(job)
            # todo: need check index out of range?
            new_scheduler = layer.schedulers[min(layer.highest_priority_scheduler_index + 1, len(layer.schedulers) - 1)]
            new_scheduler.add_new_job(job)
