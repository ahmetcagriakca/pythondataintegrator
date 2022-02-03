from injector import inject
from pdip.cqrs import Dispatcher
from pdip.cqrs import IQueryHandler
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped

from src.application.dashboard.GetConnectionWidget.GetConnectionWidgetQuery import GetConnectionWidgetQuery
from src.application.dashboard.GetDailyExecutionsWidget.GetDailyExecutionsWidgetQuery import \
    GetDailyExecutionsWidgetQuery
from src.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsQuery import GetDashboardWidgetsQuery
from src.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsResponse import GetDashboardWidgetsResponse
from src.application.dashboard.GetDashboardWidgets.GetDashboardWidgetsSpecifications import \
    GetDashboardWidgetsSpecifications
from src.application.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetQuery import \
    GetDataOperationJobExecutionWidgetQuery
from src.application.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetQuery import \
    GetDataOperationJobWidgetQuery
from src.application.dashboard.GetDataOperationWidget.GetDataOperationWidgetQuery import GetDataOperationWidgetQuery
from src.application.dashboard.GetExecutionStatusesWidget.GetExecutionStatusesWidgetQuery import \
    GetExecutionStatusesWidgetQuery
from src.application.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetQuery import \
    GetMonthlyExecutionsWidgetQuery
from src.application.dashboard.GetSourceDataAffectedRowWidget.GetSourceDataAffectedRowWidgetQuery import \
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

        daily_executions_widget_data = self.dispatcher.dispatch(GetDailyExecutionsWidgetQuery())
        result.Data.append(daily_executions_widget_data.Data.WidgetData)

        execution_statuses_widget_data = self.dispatcher.dispatch(GetExecutionStatusesWidgetQuery())
        result.Data.append(execution_statuses_widget_data.Data.WidgetData)
        return result
