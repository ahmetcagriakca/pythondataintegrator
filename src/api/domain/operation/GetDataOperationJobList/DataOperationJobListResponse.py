from dataclasses import dataclass
from typing import List

from domain.operation.GetDataOperationJobList.DataOperationJobListDto import DataOperationJobListDto
from infrastructure.json.JsonConvert import JsonConvert


@JsonConvert.register
@dataclass
class DataOperationJobListResponse:
    PageData: List[DataOperationJobListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None

    def to_dict(self):
        dic = self.__dict__
        dic["PageData"] = [entity.to_dict() for entity in self.PageData]
        return dic
