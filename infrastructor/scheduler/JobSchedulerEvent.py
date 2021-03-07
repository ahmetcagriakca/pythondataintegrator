import jsonpickle
from infrastructor.IocManager import IocManager
from infrastructor.scheduler.JobSchedulerService import JobSchedulerService


class JobSchedulerEvent:
    job_scheduler_type = None

    # handle transaction and handle unexpected errors
    def event_service_handler(func):
        def inner(*args, **kwargs):
            service = JobSchedulerService()
            if service.job_scheduler_type is None:
                service.set_job_scheduler_type(job_scheduler_type=JobSchedulerEvent.job_scheduler_type)
            result = func(service=service, event=args[0], **kwargs)
            del service
            return result
        return inner

    @staticmethod
    @event_service_handler
    def listener_job_added(service: JobSchedulerService, event, *args, **kwargs):
        job = service.get_job(event.job_id)
        service.add_job(event)
        service.add_job_event(event)
        service.add_log(event, f'{job.name} added with funct_ref:{job.func_ref}, max_instances:{job.max_instances}')

    @staticmethod
    @event_service_handler
    def listener_job_removed(service: JobSchedulerService, event, *args, **kwargs):
        service.add_job_event(event)
        service.remove_job(event)
        service.add_log(event, f'Job removed')

    @staticmethod
    @event_service_handler
    def listener_all_jobs_removed(service: JobSchedulerService, event, *args, **kwargs):
        service.add_job_event(event)
        service.remove_job(event)
        service.add_log(event, f'Jobs removed')

    @staticmethod
    @event_service_handler
    def listener_finish(service: JobSchedulerService, event, *args, **kwargs):
        if hasattr(event, 'exception') and event.exception:
            service.add_job_event(event)
            if hasattr(event, 'traceback') and event.traceback:
                service.add_log(event,
                                f'exception:{event.exception} traceback:{event.traceback}')
            else:
                service.add_log(event, f'exception:{event.exception}')
        else:
            service.add_job_event(event)
            retval = None
            if hasattr(event, 'retval') and event.retval:
                retval = event.retval
            retval_string = jsonpickle.encode(retval)
            service.add_log(event, f'return value:{retval_string}')

    @staticmethod
    @event_service_handler
    def listener_job_submitted(service: JobSchedulerService, event, *args, **kwargs):
        job = service.get_job(event.job_id)
        next_run_time = None
        if hasattr(job, 'next_run_time') and job.next_run_time:
            next_run_time = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        service.add_job_event(event)
        service.update_job(event)
        service.add_log(event, f'Next Run Time:{next_run_time}')

    @staticmethod
    @event_service_handler
    def listener_job_others(service: JobSchedulerService, event, *args, **kwargs):
        service.add_job_event(event)
        service.add_log(event, f'')

    @staticmethod
    @event_service_handler
    def listener_scheduler_other_events(service: JobSchedulerService, event, *args, **kwargs):
        service.add_log(event, f'')
