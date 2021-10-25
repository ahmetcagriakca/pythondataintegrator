from traceback import format_exc
from apscheduler.events import EVENT_JOB_MISSED
from injector import inject
from pdip.dependency.container import DependencyContainer
from queue import Queue

from scheduler.application.operation.commands.SendMissMailCommand import SendMissMailCommand


class JobEventHandler:
    @inject
    def __init__(self,

                 ):
        pass

    @staticmethod
    def start_job_event_handler_process(sub_process_id,
                                        event_queue: Queue) -> int:
        return DependencyContainer.Instance.get(JobEventHandler).start_job_event_handler(
            event_queue=event_queue
        )

    def start_job_event_handler(self, event_queue: Queue):
        while True:
            event = event_queue.get()
            try:
                if event.code == EVENT_JOB_MISSED:
                    command = SendMissMailCommand()
                    command.send(job_id=event.job_id)
                    del command
            except Exception as ex:
                formatted_exception=format_exc()
                self.sql_logger.error(f"Job event getting error. Error:{ex}- Traceback:{formatted_exception}")
        return inner
