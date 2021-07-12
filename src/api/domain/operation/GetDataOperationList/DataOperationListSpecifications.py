from injector import inject
from sqlalchemy.orm import Query

from domain.common.specifications.OrderBySpecification import OrderBySpecification
from domain.common.specifications.PagingSpecification import PagingSpecification
from domain.operation.GetDataOperationList.DataOperationListQuery import DataOperationListQuery
from models.dao.operation import DataOperationContact, DataOperation, Definition


class DataOperationListSpecifications:
    @inject
    def __init__(self,
                 order_by_specification: OrderBySpecification,
                 paging_specification: PagingSpecification,
                 ):
        self.paging_specification = paging_specification
        self.order_by_specification = order_by_specification

    def specify(self, data_query: Query, query: DataOperationListQuery) -> Query:
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

    def __specified_query(self, query: DataOperationListQuery, data_query: Query) -> Query:
        specified_query = data_query \
            .join(Definition)
        if query.request.Id is not None:
            specified_query = specified_query.filter(DataOperation.Id == query.request.Id)
        return specified_query

    def count(self, query: DataOperationListQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
