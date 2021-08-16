from dataclasses import dataclass

from domain.schedule.DeleteCronJob.DeleteCronJobRequest import DeleteCronJobRequest
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class DeleteCronJobCommand(ICommand):
    request: DeleteCronJobRequest = None
