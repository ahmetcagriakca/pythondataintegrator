from injector import inject
from sqlalchemy.orm import Query

from domain.common.specifications.OrderBySpecification import OrderBySpecification
from domain.common.specifications.PagingSpecification import PagingSpecification
from domain.operation.GetDataOperationJobList.GetDataOperationJobListQuery import GetDataOperationJobListQuery

from models.dao.aps import ApSchedulerJob
from models.dao.operation import DataOperation, Definition, DataOperationJob


class GetDataOperationJobListSpecifications:
    @inject
    def __init__(self,
                 order_by_specification: OrderBySpecification,
                 paging_specification: PagingSpecification,
                 ):
        self.paging_specification = paging_specification
        self.order_by_specification = order_by_specification

    def specify(self, data_query: Query, query: GetDataOperationJobListQuery) -> Query:
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

    def __specified_query(self, query: GetDataOperationJobListQuery, data_query: Query) -> Query:
        specified_query = data_query \
            .join(DataOperation) \
            .join(ApSchedulerJob)

        if query.request.DataOperationId is not None and query.request.DataOperationId != '':
            specified_query = specified_query.filter(DataOperation.Id == query.request.DataOperationId)

        if query.request.DataOperationName is not None and query.request.DataOperationName != '':
            specified_query = specified_query.filter(DataOperation.Name == query.request.DataOperationName)

        if query.request.OnlyCron is not None and query.request.OnlyCron:
            specified_query = specified_query.filter(DataOperationJob.Cron != None)

        if query.request.OnlyUndeleted is not None and query.request.OnlyUndeleted:
            specified_query = specified_query.filter(DataOperationJob.IsDeleted == 0)
        return specified_query

    def count(self, query: GetDataOperationJobListQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
