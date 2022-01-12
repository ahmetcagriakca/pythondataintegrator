from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.data.seed import Seed
from pdip.logging.loggers.sql import SqlLogger

from src.domain.aps.ApSchedulerEvent import ApSchedulerEvent
from src.domain.enums.apschedulerevents import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN, \
    EVENT_SCHEDULER_PAUSED, EVENT_SCHEDULER_RESUMED, EVENT_EXECUTOR_ADDED, EVENT_EXECUTOR_REMOVED, \
    EVENT_JOBSTORE_ADDED, EVENT_JOBSTORE_REMOVED, EVENT_ALL_JOBS_REMOVED, EVENT_JOB_ADDED, EVENT_JOB_REMOVED, \
    EVENT_JOB_MODIFIED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_SUBMITTED, \
    EVENT_JOB_MAX_INSTANCES


class ApSchedulerSeed(Seed):
    @inject
    def __init__(
            self,
            repository_provider: RepositoryProvider,
            logger: SqlLogger,
    ):
        self.logger = logger
        self.repository_provider = repository_provider

    def seed(self):
        try:
            ap_scheduler_event_repository = self.repository_provider.get(ApSchedulerEvent)
            check_count = ap_scheduler_event_repository.table.count()
            if check_count is None or check_count == 0:

                events_list = [
                    {
                        "Code": EVENT_SCHEDULER_STARTED,
                        "Name": "EVENT_SCHEDULER_STARTED",
                        "Description": "The scheduler was started",
                        "Class": "SchedulerEvent"
                    },
                    {
                        "Code": EVENT_SCHEDULER_SHUTDOWN,
                        "Name": "EVENT_SCHEDULER_SHUTDOWN",
                        "Description": "The scheduler was shut down",
                        "Class": "SchedulerEvent"
                    },
                    {
                        "Code": EVENT_SCHEDULER_PAUSED,
                        "Name": "EVENT_SCHEDULER_PAUSED",
                        "Description": "Job processing in the scheduler was paused",
                        "Class": "SchedulerEvent"
                    },
                    {
                        "Code": EVENT_SCHEDULER_RESUMED,
                        "Name": "EVENT_SCHEDULER_RESUMED",
                        "Description": "Job processing in the scheduler was resumed",
                        "Class": "SchedulerEvent"
                    },
                    {
                        "Code": EVENT_EXECUTOR_ADDED,
                        "Name": "EVENT_EXECUTOR_ADDED",
                        "Description": "An executor was added to the scheduler",
                        "Class": "SchedulerEvent"
                    },
                    {
                        "Code": EVENT_EXECUTOR_REMOVED,
                        "Name": "EVENT_EXECUTOR_REMOVED",
                        "Description": "An executor was removed to the scheduler",
                        "Class": "SchedulerEvent"
                    },
                    {
                        "Code": EVENT_JOBSTORE_ADDED,
                        "Name": "EVENT_JOBSTORE_ADDED",
                        "Description": "A job store was added to the scheduler",
                        "Class": "SchedulerEvent"
                    },
                    {
                        "Code": EVENT_JOBSTORE_REMOVED,
                        "Name": "EVENT_JOBSTORE_REMOVED",
                        "Description": "A job store was removed from the scheduler",
                        "Class": "SchedulerEvent"
                    },
                    {
                        "Code": EVENT_ALL_JOBS_REMOVED,
                        "Name": "EVENT_ALL_JOBS_REMOVED",
                        "Description": "All jobs were removed from either all job stores or one particular job store",
                        "Class": "SchedulerEvent"
                    },
                    {
                        "Code": EVENT_JOB_ADDED,
                        "Name": "EVENT_JOB_ADDED",
                        "Description": "A job was added to a job store",
                        "Class": "JobEvent"
                    },
                    {
                        "Code": EVENT_JOB_REMOVED,
                        "Name": "EVENT_JOB_REMOVED",
                        "Description": "A job was removed from a job store",
                        "Class": "JobEvent"
                    },
                    {
                        "Code": EVENT_JOB_MODIFIED,
                        "Name": "EVENT_JOB_MODIFIED",
                        "Description": "A job was modified from outside the scheduler",
                        "Class": "JobEvent"
                    },
                    {
                        "Code": EVENT_JOB_EXECUTED,
                        "Name": "EVENT_JOB_EXECUTED",
                        "Description": "A job was executed successfully",
                        "Class": "JobExecutionEvent"
                    },
                    {
                        "Code": EVENT_JOB_ERROR,
                        "Name": "EVENT_JOB_ERROR",
                        "Description": "A job raised an exception during execution",
                        "Class": "JobExecutionEvent"
                    },
                    {
                        "Code": EVENT_JOB_MISSED,
                        "Name": "EVENT_JOB_MISSED",
                        "Description": "A job’s execution was missed",
                        "Class": "JobExecutionEvent"
                    },
                    {
                        "Code": EVENT_JOB_SUBMITTED,
                        "Name": "EVENT_JOB_SUBMITTED",
                        "Description": "A job was submitted to its executor to be run",
                        "Class": "JobSubmissionEvent"
                    },
                    {
                        "Code": EVENT_JOB_MAX_INSTANCES,
                        "Name": "EVENT_JOB_MAX_INSTANCES",
                        "Description": "A job being submitted to its executor was not accepted by the executor because the job has already reached its maximum concurrently executing instances",
                        "Class": "JobSubmissionEvent"
                    }
                ]
                for eventJson in events_list:
                    event = ApSchedulerEvent(Code=eventJson["Code"], Name=eventJson["Name"],
                                             Description=eventJson["Description"],
                                             Class=eventJson["Class"])
                    ap_scheduler_event_repository.insert(event)
                    self.repository_provider.commit()
        except Exception as ex:
            self.logger.exception(ex, "ApScheduler seeds getting error")
