from datetime import datetime

import rpyc
from injector import inject
from pdip.dependency import IScoped
from pdip.logging.loggers.database import SqlLogger

from pdi.domain.aps.ApSchedulerJob import ApSchedulerJob
from pdi.domain.configs.SchedulerRpcClientConfig import SchedulerRpcClientConfig


class SchedulerRpcClientService(IScoped):

    @inject
    def __init__(self,
                 scheduler_rpc_client_config: SchedulerRpcClientConfig,
                 sql_logger: SqlLogger,
                 ):
        self.scheduler_rpc_client_config = scheduler_rpc_client_config
        self.sql_logger = sql_logger

    def connect_rpc(self):
        conn = rpyc.connect(self.scheduler_rpc_client_config.host, self.scheduler_rpc_client_config.port)
        return conn

    def delete_job(self, ap_scheduler_table_job_id):
        conn = self.connect_rpc()
        job = conn.root.remove_job(ap_scheduler_table_job_id)
        return job

    def add_job_with_cron(self, cron, start_date=None, end_date=None, args=None, kwargs=None):
        conn = self.connect_rpc()
        job = conn.root.add_job_with_cron(cron, start_date.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ") if start_date is not None else datetime.now().astimezone().strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"),
                                          end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if end_date is not None else None,
                                          args=args, kwargs=kwargs)
        return job

    def add_job_with_date(self, run_date, args=None, kwargs=None) -> ApSchedulerJob:
        conn = self.connect_rpc()
        job = conn.root.add_job_with_date(run_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), args=args, kwargs=kwargs)
        return job
