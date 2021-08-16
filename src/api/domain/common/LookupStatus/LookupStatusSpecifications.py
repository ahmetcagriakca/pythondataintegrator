from injector import inject
from sqlalchemy.orm import Query
from infrastructure.dependency.scopes import IScoped
from domain.common.LookupStatus.LookupStatusQuery import LookupStatusQuery


class LookupStatusSpecifications(IScoped):
    @inject
    def __init__(self,
                 ):
        pass

    def __specified_query(self, query: LookupStatusQuery, data_query: Query) -> Query:
        specified_query = data_query 
        # TODO:specify query
        return specified_query
        
    def specify(self, data_query: Query, query: LookupStatusQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)
        return data_query

    def count(self, query: LookupStatusQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
