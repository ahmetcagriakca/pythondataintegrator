from dataclasses import dataclass
from pdip.cqrs import IQuery

from pdi.application.connection.LookupConnection.LookupConnectionRequest import LookupConnectionRequest
from pdi.application.connection.LookupConnection.LookupConnectionResponse import LookupConnectionResponse


@dataclass
class LookupConnectionQuery(IQuery[LookupConnectionResponse]):
    request: LookupConnectionRequest = None
