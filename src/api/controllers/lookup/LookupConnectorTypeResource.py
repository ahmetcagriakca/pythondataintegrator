from injector import inject
from domain.connection.LookupConnectorType.LookupConnectorTypeQuery import LookupConnectorTypeQuery
from domain.connection.LookupConnectorType.LookupConnectorTypeRequest import LookupConnectorTypeRequest
from domain.connection.LookupConnectorType.LookupConnectorTypeResponse import LookupConnectorTypeResponse
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.api.decorators.Controller import controller
from infrastructure.cqrs.Dispatcher import Dispatcher


@controller()
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
