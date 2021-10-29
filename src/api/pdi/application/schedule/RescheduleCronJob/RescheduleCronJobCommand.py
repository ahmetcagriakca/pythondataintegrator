from dataclasses import dataclass
from pdip.cqrs import ICommand

from pdi.application.schedule.RescheduleCronJob.RescheduleCronJobRequest import RescheduleCronJobRequest


@dataclass
class RescheduleCronJobCommand(ICommand):
    request: RescheduleCronJobRequest = None
