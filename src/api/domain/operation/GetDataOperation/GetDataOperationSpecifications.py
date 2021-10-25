from injector import inject
from sqlalchemy.orm import Query
from pdip.dependency import IScoped
from domain.operation.GetDataOperation.GetDataOperationQuery import GetDataOperationQuery
from models.dao.operation import Definition, DataOperation


class GetDataOperationSpecifications(IScoped):
    @inject
    def __init__(self,
                 ):
        pass

    def __specified_query(self, query: GetDataOperationQuery, data_query: Query) -> Query:
        specified_query = data_query \
            .join(Definition, isouter=True)
        specified_query = specified_query.filter(DataOperation.Id == query.request.Id)
        return specified_query

    def specify(self, data_query: Query, query: GetDataOperationQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)
        return data_query

    def count(self, query: GetDataOperationQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
