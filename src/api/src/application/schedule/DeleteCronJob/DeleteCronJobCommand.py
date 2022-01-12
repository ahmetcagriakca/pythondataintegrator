from dataclasses import dataclass
from pdip.cqrs import ICommand

from src.application.schedule.DeleteCronJob.DeleteCronJobRequest import DeleteCronJobRequest


@dataclass
class DeleteCronJobCommand(ICommand):
    request: DeleteCronJobRequest = None
