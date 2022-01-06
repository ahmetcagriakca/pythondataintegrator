from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from pdi.application.dashboard.GetConnectionWidget.GetConnectionWidgetQuery import GetConnectionWidgetQuery
from pdi.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsQuery import GetDashboardWidgetsQuery
from pdi.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsResponse import GetDashboardWidgetsResponse
from pdi.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsSpecifications import \
    GetDashboardWidgetsSpecifications
from pdi.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetQuery import \
    GetDataOperationJobExecutionWidgetQuery
from pdi.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetQuery import \
    GetDataOperationJobWidgetQuery
from pdi.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetQuery import GetDataOperationWidgetQuery
from pdi.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetQuery import \
    GetMonthlyExecutionsWidgetQuery
from pdi.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetQuery import \
    GetSourceDataAffectedRowWidgetQuery


class GetDashboardWidgetsQueryHandler(IQueryHandler[GetDashboardWidgetsQuery], IScoped):
    @inject
    def __init__(self,
                 dispatcher: Dispatcher,
                 repository_provider: RepositoryProvider,
                 specifications: GetDashboardWidgetsSpecifications):
        self.dispatcher = dispatcher
        self.repository_provider = repository_provider
        self.specifications = specifications

    def handle(self, query: GetDashboardWidgetsQuery) -> GetDashboardWidgetsResponse:
        result = GetDashboardWidgetsResponse()
        result.Data = []

        connection_widget_data = self.dispatcher.dispatch(GetConnectionWidgetQuery())
        result.Data.append(connection_widget_data.Data.WidgetData)

        data_operation_widget_data = self.dispatcher.dispatch(GetDataOperationWidgetQuery())
        result.Data.append(data_operation_widget_data.Data.WidgetData)

        data_operation_job_widget_data = self.dispatcher.dispatch(GetDataOperationJobWidgetQuery())
        result.Data.append(data_operation_job_widget_data.Data.WidgetData)

        data_operation_job_execution_widget_data = self.dispatcher.dispatch(GetDataOperationJobExecutionWidgetQuery())
        result.Data.append(data_operation_job_execution_widget_data.Data.WidgetData)

        monthly_executions_widget_data = self.dispatcher.dispatch(GetMonthlyExecutionsWidgetQuery())
        result.Data.append(monthly_executions_widget_data.Data.WidgetData)

        source_data_affected_row_widget_data = self.dispatcher.dispatch(GetSourceDataAffectedRowWidgetQuery())
        result.Data.append(source_data_affected_row_widget_data.Data.WidgetData)
        return result
