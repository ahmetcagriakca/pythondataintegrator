from dataclasses import dataclass

from domain.schedule.DeleteCronJob.DeleteCronJobRequest import DeleteCronJobRequest
from pdip.cqrs import ICommand


@dataclass
class DeleteCronJobCommand(ICommand):
    request: DeleteCronJobRequest = None
