from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.connection.GetConnectionBigData.GetConnectionBigDataRequest import GetConnectionBigDataRequest
from src.application.connection.GetConnectionBigData.GetConnectionBigDataResponse import GetConnectionBigDataResponse


@dataclass
class GetConnectionBigDataQuery(IQuery[GetConnectionBigDataResponse]):
    request: GetConnectionBigDataRequest = None
