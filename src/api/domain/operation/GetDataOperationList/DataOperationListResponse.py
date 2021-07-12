from dataclasses import dataclass
from typing import List

from domain.operation.GetDataOperationList.DataOperationListDto import DataOperationListDto
from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
@dataclass
class DataOperationListResponse:
    DataOperations: List[DataOperationListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None

    def to_dict(self):
        dic=self.__dict__
        dic["DataOperations"]=[entity.to_dict() for entity in self.DataOperations]
        return dic
