from injector import inject
from pdip.cqrs import IQueryHandler
from pdip.dependency import IScoped

from src.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetMapping import \
    GetSourceDataAffectedRowWidgetMapping
from src.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetQuery import \
    GetSourceDataAffectedRowWidgetQuery
from src.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetResponse import \
    GetSourceDataAffectedRowWidgetResponse
from src.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetSpecifications import \
    GetSourceDataAffectedRowWidgetSpecifications


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
