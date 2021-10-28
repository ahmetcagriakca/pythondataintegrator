from pdip.data import EntityBase


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
