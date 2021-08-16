from dataclasses import dataclass
from infrastructure.cqrs.ICommand import ICommand
from domain.schedule.ScheduleJob.ScheduleJobRequest import ScheduleJobRequest


@dataclass
class ScheduleJobCommand(ICommand):
    # TODO:Command attributes
    request: ScheduleJobRequest = None
    pass
