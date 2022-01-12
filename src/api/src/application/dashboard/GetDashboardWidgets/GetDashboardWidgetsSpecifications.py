from injector import inject
from pdip.dependency import IScoped
from sqlalchemy.orm import Query

from src.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsQuery import GetDashboardWidgetsQuery


class GetDashboardWidgetsSpecifications(IScoped):
    @inject
    def __init__(self,
                 ):
        pass

    def __specified_query(self, query: GetDashboardWidgetsQuery, data_query: Query) -> Query:
        specified_query = data_query
        # TODO:specify query
        return specified_query

    def specify(self, data_query: Query, query: GetDashboardWidgetsQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)
        return data_query

    def count(self, query: GetDashboardWidgetsQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
