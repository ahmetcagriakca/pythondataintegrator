from dataclasses import dataclass
from typing import Optional

from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter
from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
@dataclass
class DataOperationJobListRequest(PagingParameter, OrderByParameter):
    DataOperationName: Optional[str] = None
    OnlyCron: Optional[bool] = None
    OnlyUndeleted: Optional[bool] = None
