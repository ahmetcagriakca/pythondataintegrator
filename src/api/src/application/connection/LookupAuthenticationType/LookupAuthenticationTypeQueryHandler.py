from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from src.application.connection.LookupAuthenticationType.LookupAuthenticationTypeMapping import \
    LookupAuthenticationTypeMapping
from src.application.connection.LookupAuthenticationType.LookupAuthenticationTypeQuery import \
    LookupAuthenticationTypeQuery
from src.application.connection.LookupAuthenticationType.LookupAuthenticationTypeResponse import \
    LookupAuthenticationTypeResponse
from src.application.connection.LookupAuthenticationType.LookupAuthenticationTypeSpecifications import \
    LookupAuthenticationTypeSpecifications


class LookupAuthenticationTypeQueryHandler(IQueryHandler[LookupAuthenticationTypeQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: LookupAuthenticationTypeSpecifications):
        self.specifications = specifications

    def handle(self, query: LookupAuthenticationTypeQuery) -> LookupAuthenticationTypeResponse:
        result = LookupAuthenticationTypeResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = LookupAuthenticationTypeMapping.to_dtos(data_query)
        return result
