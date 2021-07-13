from dataclasses import dataclass

from domain.operation.GetDataOperationJobList.DataOperationJobListRequest import DataOperationJobListRequest


@dataclass
class DataOperationJobListQuery:
    request: DataOperationJobListRequest= None
