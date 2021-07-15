from typing import List

from domain.common.decorators.responseclass import responseclass
from domain.connection.GetConnectionList.GetConnectionListDto import GetConnectionListDto


@responseclass
class GetConnectionListResponse:
    PageData: List[GetConnectionListDto] = None
    PageNumber: int = None
    PageSize: int = None
    Count: int = None

    # def to_dict(self):
    #     dic = self.__dict__
    #     dic["PageData"] = [entity.to_dict() for entity in self.PageData]
    #     return dic
