from queue import Queue
from traceback import format_exc

from apscheduler.events import EVENT_JOB_MISSED
from injector import inject
from pdip.cqrs import Dispatcher
from pdip.dependency import ISingleton
from pdip.dependency.container import DependencyContainer
from pdip.logging.loggers.sql import SqlLogger

from scheduler.application.SendMissMail.SendMissMailCommand import SendMissMailCommand


class JobEventHandler(ISingleton):
    @inject
    def __init__(self,
                 logger: SqlLogger,
                 dispatcher: Dispatcher,
                 ):
        self.dispatcher = dispatcher
        self.logger = logger

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
                    command = SendMissMailCommand(JobId=event.job_id)
                    self.dispatcher.dispatch(command)
            except Exception as ex:
                formatted_exception = format_exc()
                self.logger.error(f"Job event getting error. Error:{ex}- Traceback:{formatted_exception}")
        return inner
