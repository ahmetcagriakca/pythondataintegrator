from dataclasses import dataclass
from domain.schedule.DeleteJob.DeleteJobRequest import DeleteJobRequest
from pdip.cqrs import ICommand


@dataclass
class DeleteJobCommand(ICommand):
    request: DeleteJobRequest = None
