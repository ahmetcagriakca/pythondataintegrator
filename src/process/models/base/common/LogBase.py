from datetime import datetime

from models.base.EntityBase import EntityBase
from infrastructor.json.BaseConverter import BaseConverter


@BaseConverter.register
class LogBase(EntityBase):

    def __init__(self,
                 TypeId: str = None,
                 Content: str = None,
                 LogDatetime: datetime = None,
                 JobId: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TypeId = TypeId
        self.Content = Content
        self.LogDatetime = LogDatetime
        self.JobId = JobId
