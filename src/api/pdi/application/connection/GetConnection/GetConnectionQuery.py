from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.connection.GetConnection.GetConnectionRequest import GetConnectionRequest
from pdi.application.connection.GetConnection.GetConnectionResponse import GetConnectionResponse


@dataclass
class GetConnectionQuery(IQuery[GetConnectionResponse]):
    request: GetConnectionRequest = None
