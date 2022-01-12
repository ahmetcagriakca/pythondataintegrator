from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from src.application.schedule.DeleteJob.DeleteJobCommand import DeleteJobCommand
from src.application.schedule.DeleteJob.DeleteJobRequest import DeleteJobRequest
from src.application.schedule.ScheduleJob.ScheduleJobCommand import ScheduleJobCommand
from src.application.schedule.ScheduleJob.ScheduleJobRequest import ScheduleJobRequest


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

    def delete(self, req: DeleteJobRequest):
        """
        Delete Existing Data Operation
        """
        command = DeleteJobCommand(request=req)
        self.dispatcher.dispatch(command)
