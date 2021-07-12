from dataclasses import dataclass
from typing import Optional

from domain.common.request_parameter.OrderByParameter import OrderByParameter
from domain.common.request_parameter.PagingParameter import PagingParameter
from infrastructor.json.JsonConvert import JsonConvert


@JsonConvert.register
@dataclass
class DataOperationListRequest(PagingParameter, OrderByParameter):
    Id: Optional[int] = None
