import jsonpickle
from infrastructor.IocManager import IocManager
from infrastructor.scheduler.JobSchedulerService import JobSchedulerService


class JobSchedulerEvent:
    job_scheduler_type = None

    @staticmethod
    def job_scheduler_service() -> JobSchedulerService:
        service = IocManager.injector.get(JobSchedulerService)
        if service.job_scheduler_type is None:
            print("job type not setted")
            service.set_job_scheduler_type(job_scheduler_type=JobSchedulerEvent.job_scheduler_type)
        return service

    @staticmethod
    def listener_job_added(event, *args, **kwargs):
        job = JobSchedulerEvent.job_scheduler_service().get_job(event.job_id)
        JobSchedulerEvent.job_scheduler_service().add_job(event)
        JobSchedulerEvent.job_scheduler_service().add_job_event(event)
        JobSchedulerEvent.job_scheduler_service().add_log(event,
                                                          f'{job.name} added with funct_ref:{job.func_ref}, max_instances:{job.max_instances}')

    @staticmethod
    def listener_job_removed(event, *args, **kwargs):
        JobSchedulerEvent.job_scheduler_service().add_job_event(event)
        JobSchedulerEvent.job_scheduler_service().remove_job(event)
        JobSchedulerEvent.job_scheduler_service().add_log(event, f'Job removed')

    @staticmethod
    def listener_all_jobs_removed(event, *args, **kwargs):
        JobSchedulerEvent.job_scheduler_service().add_job_event(event)
        JobSchedulerEvent.job_scheduler_service().remove_job(event)
        JobSchedulerEvent.job_scheduler_service().add_log(event, f'Jobs removed')

    @staticmethod
    def listener_finish(event, *args, **kwargs):
        if hasattr(event, 'exception') and event.exception:
            JobSchedulerEvent.job_scheduler_service().add_job_event(event)
            if hasattr(event, 'traceback') and event.traceback:
                JobSchedulerEvent.job_scheduler_service().add_log(event,
                                                                  f'exception:{event.exception} traceback:{event.traceback}')
            else:
                JobSchedulerEvent.job_scheduler_service().add_log(event, f'exception:{event.exception}')
        else:
            JobSchedulerEvent.job_scheduler_service().add_job_event(event)
            retval = None
            if hasattr(event, 'retval') and event.retval:
                retval = event.retval
            retval_string = jsonpickle.encode(retval)
            JobSchedulerEvent.job_scheduler_service().add_log(event, f'return value:{retval_string}')

    @staticmethod
    def listener_job_submitted(event, *args, **kwargs):
        job = JobSchedulerEvent.job_scheduler_service().get_job(event.job_id)
        next_run_time = None
        if hasattr(job, 'next_run_time') and job.next_run_time:
            next_run_time = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        JobSchedulerEvent.job_scheduler_service().add_job_event(event)
        JobSchedulerEvent.job_scheduler_service().update_job(event)
        JobSchedulerEvent.job_scheduler_service().add_log(event, f'Next Run Time:{next_run_time}')

    @staticmethod
    def listener_job_others(event, *args, **kwargs):
        JobSchedulerEvent.job_scheduler_service().add_job_event(event)
        JobSchedulerEvent.job_scheduler_service().add_log(event, f'')

    @staticmethod
    def listener_scheduler_other_events(event, *args, **kwargs):
        JobSchedulerEvent.job_scheduler_service().add_log(event, f'')
