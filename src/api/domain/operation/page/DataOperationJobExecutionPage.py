from injector import inject
from sqlalchemy import func

from pdip.html import HtmlTemplateService, Pagination
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from models.dao.operation import DataOperationJobExecution, \
    DataOperationJobExecutionIntegration, DataOperationJobExecutionIntegrationEvent


class DataOperationJobExecutionPage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render_job_execution(self, pagination):
        headers = [
            {'value': 'Execution Id'},
            {'value': 'Job Id'},
            {'value': 'Name'},
            {'value': 'Schedule Info'},
            {'value': 'Status'},
            {'value': 'Log'},
            {'value': 'Source Data Count'},
            {'value': 'Affected Row Count'},
            {'value': 'Execution Start Date'},
            {'value': 'Execution End Date'}
        ]

        def prepare_row(data: DataOperationJobExecution):
            max_id = self.repository_provider.query(
                func.max(DataOperationJobExecutionIntegration.Id)) \
                .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == data.Id)
            error_integration = self.repository_provider.get(DataOperationJobExecutionIntegration).first(Id=max_id)
            error_log = ''
            if error_integration is not None and error_integration.Log is not None:
                error_log = error_integration.Log.replace('\n', '<br />').replace('\t',
                                                                                  '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            total_source_data_count = self.repository_provider.query(
                func.sum(DataOperationJobExecutionIntegration.SourceDataCount).label("SourceDataCount")) \
                .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == data.Id).first()[0]
            if total_source_data_count is None or total_source_data_count < 0:
                total_source_data_count = 0

            total_affected_row = self.repository_provider.query(
                func.sum(DataOperationJobExecutionIntegrationEvent.AffectedRowCount).label("AffectedRowCount")) \
                .join(DataOperationJobExecutionIntegration.DataOperationJobExecutionIntegrationEvents) \
                .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == data.Id).first()[0]
            if total_affected_row is None or total_affected_row < 0:
                total_affected_row = 0

            end_date = ''
            if data.EndDate is not None:
                end_date = data.EndDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            row = {
                'data':
                    [
                        {
                            'value': f'<a href="/DataOperation/Job/Execution/{data.Id}">{data.Id}</a>-<a href="/DataOperation/Job/Execution/Log/{data.Id}">log</a>'},
                        {
                            'value': f'<a href="/DataOperation/Job/{data.DataOperationJob.Id}">{data.DataOperationJob.Id}</a>'},
                        {
                            'value': f'<a href="/DataOperation/{data.DataOperationJob.DataOperation.Id}">{data.DataOperationJob.DataOperation.Name}({data.DataOperationJob.DataOperation.Id})</a>'},
                        {
                            'value': f'{data.DataOperationJob.Cron}({data.DataOperationJob.StartDate}-{data.DataOperationJob.EndDate})'},
                        {'value': data.Status.Description},
                        {'value': error_log},
                        {'value': total_source_data_count},
                        {'value': total_affected_row},
                        {'value': data.StartDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                         'class': 'column-nowrap'},
                        {'value': end_date,
                         'class': 'column-nowrap'}
                    ]
            }
            return row

        data_operation_job_execution_repository = self.repository_provider.get(DataOperationJobExecution)

        query = data_operation_job_execution_repository.table

        if pagination.Filter is not None and pagination.Filter != '':
            if pagination.Filter == '0':
                query = query.filter(DataOperationJobExecution.StatusId != 3)
            elif pagination.Filter in ['1', '2', '3', '4']:
                status_id = int(pagination.Filter)
                query = query.filter(DataOperationJobExecution.StatusId == status_id)
        pagination.PageUrl = '/DataOperation/Job/Execution{}'
        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           sortable='"Id" desc',
                                                                           pagination=pagination)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def render(self, pagination: Pagination):
        if pagination is None:
            pagination = Pagination(Limit=50)
        elif pagination.Limit is None:
            pagination.Limit = 50
        table_job = self.render_job_execution(pagination)
        return self.html_template_service.render_html(
            content=f'''  <div style="font-size: 24px;"><b>Job Executions </b></div>{table_job}''')
