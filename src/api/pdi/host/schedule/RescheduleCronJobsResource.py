from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.schedule.RescheduleCronJobs.RescheduleCronJobsCommand import RescheduleCronJobsCommand
from pdi.application.schedule.RescheduleCronJobs.RescheduleCronJobsRequest import RescheduleCronJobsRequest


class RescheduleCronJobsResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def post(self, req: RescheduleCronJobsRequest):
        """
        Schedule Data Operation Job
        """
        command = RescheduleCronJobsCommand(request=req)
        self.dispatcher.dispatch(command)
