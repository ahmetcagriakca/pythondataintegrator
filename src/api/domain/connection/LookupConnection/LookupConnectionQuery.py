from dataclasses import dataclass
from infrastructure.cqrs.IQuery import IQuery
from domain.connection.LookupConnection.LookupConnectionRequest import LookupConnectionRequest
from domain.connection.LookupConnection.LookupConnectionResponse import LookupConnectionResponse


@dataclass
class LookupConnectionQuery(IQuery[LookupConnectionResponse]):
    request: LookupConnectionRequest = None
