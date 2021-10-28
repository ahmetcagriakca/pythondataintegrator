from datetime import datetime

from pdip.data import EntityBase


class DataOperationJobExecutionEventBase(EntityBase):

    def __init__(self,
                 DataOperationJobExecutionId: int = None,
                 EventId: int = None,
                 EventDate: datetime = None,
                 Event=None,
                 DataOperationJobExecution=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutionId: int = DataOperationJobExecutionId
        self.EventId: int = EventId
        self.EventDate: int = EventDate
        self.DataOperationJobExecution = DataOperationJobExecution
        self.Event = Event
