from injector import inject
from sqlalchemy import text
from sqlalchemy.orm import Query
from pdip.dependency import IScoped
from domain.connection.LookupConnectionType.LookupConnectionTypeQuery import LookupConnectionTypeQuery


class LookupConnectionTypeSpecifications(IScoped):
    @inject
    def __init__(self,
                 ):
        pass

    def __specified_query(self, query: LookupConnectionTypeQuery, data_query: Query) -> Query:
        specified_query = data_query.order_by(text('"Id" asc'))
        return specified_query
        
    def specify(self, data_query: Query, query: LookupConnectionTypeQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)
        return data_query

    def count(self, query: LookupConnectionTypeQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
