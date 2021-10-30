from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.schedule.DeleteCronJob.DeleteCronJobCommand import DeleteCronJobCommand
from pdi.application.schedule.DeleteCronJob.DeleteCronJobRequest import DeleteCronJobRequest
from pdi.application.schedule.ScheduleCronJob.ScheduleCronJobCommand import ScheduleCronJobCommand
from pdi.application.schedule.ScheduleCronJob.ScheduleCronJobRequest import ScheduleCronJobRequest


class ScheduleCronJobResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: ScheduleCronJobRequest):
        """
        Schedule Data Operation Job
        """
        command = ScheduleCronJobCommand(request=req)
        self.dispatcher.dispatch(command)

    def delete(self, req: DeleteCronJobRequest):
        """
        Delete Existing Data Operation
        """
        command = DeleteCronJobCommand(request=req)
        self.dispatcher.dispatch(command)
