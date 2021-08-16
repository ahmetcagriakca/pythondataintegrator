from models.base.EntityBase import EntityBase
from infrastructure.json.BaseConverter import BaseConverter


@BaseConverter.register
class ApSchedulerJobEventBase(EntityBase):
    def __init__(self,
                 EventId: int = None,
                 ApSchedulerJobId: str = None,
                 ApSchedulerJob=None,
                 ApSchedulerEvent=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.EventId: int = EventId
        self.ApSchedulerJobId: str = ApSchedulerJobId
        self.ApSchedulerJob = ApSchedulerJob
        self.ApSchedulerEvent = ApSchedulerEvent
