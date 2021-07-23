from dataclasses import dataclass
from infrastructure.cqrs.IQuery import IQuery
from domain.connection.GetConnection.GetConnectionRequest import GetConnectionRequest
from domain.connection.GetConnection.GetConnectionResponse import GetConnectionResponse


@dataclass
class GetConnectionQuery(IQuery[GetConnectionResponse]):
    request: GetConnectionRequest = None
