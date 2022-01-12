from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.schedule.RescheduleCronJobs.RescheduleCronJobsRequest import RescheduleCronJobsRequest


@dataclass
class RescheduleCronJobsCommand(ICommand):
    request: RescheduleCronJobsRequest = None
