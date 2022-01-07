from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataRequest import GetConnectionBigDataRequest
from pdi.application.connection.GetConnectionBigData.GetConnectionBigDataResponse import GetConnectionBigDataResponse


@dataclass
class GetConnectionBigDataQuery(IQuery[GetConnectionBigDataResponse]):
    request: GetConnectionBigDataRequest = None
