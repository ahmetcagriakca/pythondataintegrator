from injector import inject
from pdip.api.base import ResourceBase
from pdip.cqrs import Dispatcher

from pdi.application.connection.LookupConnectorType.LookupConnectorTypeQuery import LookupConnectorTypeQuery
from pdi.application.connection.LookupConnectorType.LookupConnectorTypeRequest import LookupConnectorTypeRequest
from pdi.application.connection.LookupConnectorType.LookupConnectorTypeResponse import LookupConnectorTypeResponse


class LookupConnectorTypeResource(ResourceBase):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dispatcher = dispatcher

    def get(self, req: LookupConnectorTypeRequest) -> LookupConnectorTypeResponse:
        """
        Get All Connector Types
        """
        query = LookupConnectorTypeQuery(request=req)
        result = self.dispatcher.dispatch(query)
        return result
