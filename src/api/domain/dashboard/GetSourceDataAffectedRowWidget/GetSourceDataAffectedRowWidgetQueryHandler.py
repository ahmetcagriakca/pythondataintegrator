from injector import inject
from domain.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetMapping import GetSourceDataAffectedRowWidgetMapping
from domain.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetQuery import GetSourceDataAffectedRowWidgetQuery
from domain.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetResponse import GetSourceDataAffectedRowWidgetResponse
from domain.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetSpecifications import GetSourceDataAffectedRowWidgetSpecifications
from infrastructure.cqrs.IQueryHandler import IQueryHandler
from infrastructure.dependency.scopes import IScoped


class GetSourceDataAffectedRowWidgetQueryHandler(IQueryHandler[GetSourceDataAffectedRowWidgetQuery], IScoped):
    @inject
    def __init__(self,
                 specifications: GetSourceDataAffectedRowWidgetSpecifications):
        self.specifications = specifications

    def handle(self, query: GetSourceDataAffectedRowWidgetQuery) -> GetSourceDataAffectedRowWidgetResponse:
        result = GetSourceDataAffectedRowWidgetResponse()
        data_query = self.specifications.specify(query=query)
        result.Data = GetSourceDataAffectedRowWidgetMapping.to_dto(data_query)
        return result
