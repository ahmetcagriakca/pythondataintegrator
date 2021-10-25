from dataclasses import dataclass
from pdip.cqrs import ICommand
from domain.schedule.ScheduleJob.ScheduleJobRequest import ScheduleJobRequest


@dataclass
class ScheduleJobCommand(ICommand):
    # TODO:Command attributes
    request: ScheduleJobRequest = None
    pass
