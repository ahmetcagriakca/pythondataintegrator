from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.schedule.ScheduleCronJob.ScheduleCronJobRequest import ScheduleCronJobRequest


@dataclass
class ScheduleCronJobCommand(ICommand):
    request: ScheduleCronJobRequest = None
