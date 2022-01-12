from dataclasses import dataclass
from pdip.cqrs import IQuery

from src.application.connection.LookupConnection.LookupConnectionRequest import LookupConnectionRequest
from src.application.connection.LookupConnection.LookupConnectionResponse import LookupConnectionResponse


@dataclass
class LookupConnectionQuery(IQuery[LookupConnectionResponse]):
    request: LookupConnectionRequest = None
