from dataclasses import dataclass
from domain.schedule.DeleteJob.DeleteJobRequest import DeleteJobRequest
from infrastructure.cqrs.ICommand import ICommand


@dataclass
class DeleteJobCommand(ICommand):
    request: DeleteJobRequest = None
