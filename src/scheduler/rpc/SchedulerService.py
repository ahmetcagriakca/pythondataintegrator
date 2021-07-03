from apscheduler.triggers.cron import CronTrigger

from IocManager import IocManager
import rpyc
from rpyc.utils.server import ThreadedServer

from models.configs.SchedulerRpcServerConfig import SchedulerRpcServerConfig
from scheduler.JobScheduler import JobScheduler
from datetime import datetime

from scheduler.JobService import JobService


class SchedulerService(rpyc.Service):
    def __init__(self):
        pass

    @property
    def job_scheduler(self):
        job_scheduler = IocManager.injector.get(JobScheduler)
        return job_scheduler

    def initialize(self, scheduler_rpc_server_config: SchedulerRpcServerConfig):
        protocol_config = scheduler_rpc_server_config.protocol_config  # {'allow_public_attrs': True, 'sync_request_timeout': 60}
        server = ThreadedServer(SchedulerService, port=scheduler_rpc_server_config.port,
                                protocol_config=protocol_config)
        try:
            server.start()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            self.job_scheduler.shutdown()

    def exposed_add_job_with_cron(self, cron, start_date, end_date, *args, **kwargs):

        trigger = CronTrigger.from_crontab(cron)
        if start_date is not None:
            trigger.start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        else:
            trigger.start_date = datetime.now().astimezone()
        if end_date is not None:
            trigger.end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        job = self.job_scheduler.add_job_with_cron(job_function=JobService.job_start_data_operation,
                                                   cron=trigger,
                                                   *args, **kwargs)
        return job

    def exposed_add_job_with_date(self, run_date, *args, **kwargs):
        run_date = datetime.strptime(run_date, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone()
        job = self.job_scheduler.add_job_with_date(job_function=JobService.job_start_data_operation,
                                                   run_date=run_date,
                                                   *args,
                                                   **kwargs)
        return job

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
