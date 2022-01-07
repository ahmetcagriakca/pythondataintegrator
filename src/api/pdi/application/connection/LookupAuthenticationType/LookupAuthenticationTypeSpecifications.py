from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy import text
from sqlalchemy.orm import Query

from pdi.application.connection.LookupAuthenticationType.LookupAuthenticationTypeQuery import \
    LookupAuthenticationTypeQuery
from pdi.domain.secret import AuthenticationType


class LookupAuthenticationTypeSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider:RepositoryProvider
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: LookupAuthenticationTypeQuery) -> Query:
        repository = self.repository_provider.get(AuthenticationType)
        data_query = repository.table
        specified_query = data_query.order_by(text('"Id" asc'))
        return specified_query

    def specify(self, query: LookupAuthenticationTypeQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: LookupAuthenticationTypeQuery) -> Query:
        return self.__specified_query(query=query).count()
