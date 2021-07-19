from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand
from domain.schedule.ScheduleCronJob.ScheduleCronJobRequest import ScheduleCronJobRequest


@dataclass
class ScheduleCronJobCommand(ICommand):
    # TODO:Command attributes
    request: ScheduleCronJobRequest = None
    pass
