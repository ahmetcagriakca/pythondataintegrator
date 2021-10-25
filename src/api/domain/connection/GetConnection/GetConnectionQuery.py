from dataclasses import dataclass
from pdip.cqrs import IQuery
from domain.connection.GetConnection.GetConnectionRequest import GetConnectionRequest
from domain.connection.GetConnection.GetConnectionResponse import GetConnectionResponse


@dataclass
class GetConnectionQuery(IQuery[GetConnectionResponse]):
    request: GetConnectionRequest = None
