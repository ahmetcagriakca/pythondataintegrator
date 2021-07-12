from dataclasses import dataclass

from domain.operation.GetDataOperationList.DataOperationListRequest import DataOperationListRequest


@dataclass
class DataOperationListQuery:
    request: DataOperationListRequest= None
