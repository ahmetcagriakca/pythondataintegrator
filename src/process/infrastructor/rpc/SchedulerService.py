from IocManager import IocManager
import rpyc
from rpyc.utils.server import ThreadedServer

from infrastructor.scheduler.JobScheduler import JobScheduler
from datetime import datetime
from domain.job.services.JobOperationService import JobOperationService


class SchedulerService(rpyc.Service):
    def __init__(self):
        self.job_scheduler: JobScheduler = None
        pass

    def initialize(self, job_scheduler):
        self.job_scheduler = job_scheduler
        protocol_config = {'allow_public_attrs': True}
        server = ThreadedServer(SchedulerService, port=7300, protocol_config=protocol_config)
        try:
            server.start()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            job_scheduler.shutdown()

    def exposed_add_job_with_cron(self, func, *args, **kwargs):
        return self.job_scheduler.add_job_with_cron(func, *args, **kwargs)

    def exposed_add_job_with_date(self, func, run_date, *args, **kwargs):
        start_date = datetime.strptime(run_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        
        job_scheduler=IocManager.injector.get(IocManager.job_scheduler)
        return job_scheduler.add_job_with_date(JobOperationService.job_start_data_operation,run_date=start_date, *args, **kwargs)

    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return self.job_scheduler.modify_job(job_id, jobstore, **changes)

    def exposed_reschedule_job(self, job_id, jobstore=None, trigger=None, **trigger_args):
        return self.job_scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def exposed_pause_job(self, job_id, jobstore=None):
        return self.job_scheduler.pause_job(job_id, jobstore)

    def exposed_resume_job(self, job_id, jobstore=None):
        return self.job_scheduler.resume_job(job_id, jobstore)

    def exposed_remove_job(self, job_id, jobstore=None):
        self.job_scheduler.remove_job(job_id, jobstore)

    def exposed_get_job(self, job_id):
        return self.job_scheduler.get_job(job_id)

    def exposed_get_jobs(self, jobstore=None):
        return self.job_scheduler.get_jobs(jobstore)
