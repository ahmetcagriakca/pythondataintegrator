import datetime
from dataclasses import dataclass
from infrastructure.json.JsonConvert import JsonConvert


@JsonConvert.register
@dataclass
class DataOperationJobListDto:
    Id: int = None
    JobId: int = None
    DataOperationId: str = None
    DataOperationName: str = None
    Cron: str = None
    StartDate: datetime.datetime = None
    EndDate: datetime.datetime = None
    NextRunTime: datetime.datetime = None
    CreationDate: datetime.datetime = None
    LastUpdatedDate: datetime.datetime = None
    IsDeleted: int = None

    def to_dict(self):
        dic = self.__dict__
        return dic
