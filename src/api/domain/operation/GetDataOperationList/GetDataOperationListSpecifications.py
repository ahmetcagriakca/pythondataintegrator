from injector import inject
from sqlalchemy.orm import Query

from domain.common.specifications.OrderBySpecification import OrderBySpecification
from domain.common.specifications.PagingSpecification import PagingSpecification
from domain.operation.GetDataOperationList.GetDataOperationListQuery import GetDataOperationListQuery
from models.dao.operation import DataOperation, Definition


class GetDataOperationListSpecifications:
    @inject
    def __init__(self,
                 order_by_specification: OrderBySpecification,
                 paging_specification: PagingSpecification,
                 ):
        self.paging_specification = paging_specification
        self.order_by_specification = order_by_specification

    def specify(self, data_query: Query, query: GetDataOperationListQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)

        order_by = self.order_by_specification.specify(order_by_parameter=query.request)
        if order_by is not None:
            data_query = data_query.order_by(order_by)

        page_size, offset = self.paging_specification.specify(paging_parameter=query.request)
        if offset is not None:
            data_query = data_query.offset(offset)
        if page_size is not None:
            data_query = data_query.limit(page_size)
        return data_query

    def __specified_query(self, query: GetDataOperationListQuery, data_query: Query) -> Query:
        specified_query = data_query \
            .join(Definition, isouter=True)

        if query.request.DataOperationName is not None and query.request.DataOperationName != '':
            specified_query = specified_query.filter(DataOperation.Name == query.request.DataOperationName)
        if query.request.OnlyUndeleted is not None and query.request.OnlyUndeleted:
            specified_query = specified_query.filter(DataOperation.IsDeleted == 0)

        return specified_query

    def count(self, query: GetDataOperationListQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
