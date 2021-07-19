from injector import inject
from domain.schedule.DeleteJob.DeleteJobCommand import DeleteJobCommand
from domain.schedule.ScheduleJob.ScheduleJobCommand import ScheduleJobCommand
from domain.schedule.ScheduleJob.ScheduleJobRequest import ScheduleJobRequest
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
class ScheduleJobResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: ScheduleJobRequest):
        """
        Schedule Data Operation Job
        """
        command = ScheduleJobCommand(request=req)
        self.dispatcher.dispatch(command)
        return "Data operation created"

    def delete(self, Id: int):
        """
        Delete Existing Data Operation
        """
        command = DeleteJobCommand(Id=Id)
        self.dispatcher.dispatch(command)
        return "Data Operation Job removed successfully"
