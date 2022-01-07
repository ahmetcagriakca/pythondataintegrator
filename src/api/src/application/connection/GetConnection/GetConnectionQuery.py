from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.connection.GetConnection.GetConnectionRequest import GetConnectionRequest
from src.application.connection.GetConnection.GetConnectionResponse import GetConnectionResponse


@dataclass
class GetConnectionQuery(IQuery[GetConnectionResponse]):
    request: GetConnectionRequest = None
