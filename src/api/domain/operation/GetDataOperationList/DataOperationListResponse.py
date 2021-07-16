from dataclasses import dataclass
from typing import List

from domain.operation.GetDataOperationList.DataOperationListDto import DataOperationListDto
from infrastructure.json.JsonConvert import JsonConvert


@JsonConvert.register
@dataclass
class DataOperationListResponse:
    PageData: List[DataOperationListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None

    def to_dict(self):
        dic = self.__dict__
        dic["PageData"] = [entity.to_dict() for entity in self.PageData]
        return dic
