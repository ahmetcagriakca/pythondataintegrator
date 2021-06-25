import traceback
from queue import Queue

from injector import inject

from IocManager import IocManager
from domain.operation.command.SendMissMailCommand import SendMissMailCommand
from apscheduler.events import EVENT_JOB_MISSED


class JobEventHandler:
    @inject
    def __init__(self,

                 ):
        pass

    @staticmethod
    def start_job_event_handler_process(sub_process_id,
                                        event_queue: Queue) -> int:
        return IocManager.injector.get(JobEventHandler).start_job_event_handler(
            event_queue=event_queue
        )

    def start_job_event_handler(self, event_queue: Queue):
        while True:
            event = event_queue.get()
            try:
                if event.code == EVENT_JOB_MISSED:
                    command=SendMissMailCommand()
                    command.send(job_id=event.job_id)
                    del command
            except Exception as ex:
                self.sql_logger.error(f"Job event getting error. Error:{ex}- Traceback:{traceback.format_exc()}")
        return inner
