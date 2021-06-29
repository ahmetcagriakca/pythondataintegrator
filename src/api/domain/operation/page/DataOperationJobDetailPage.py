from injector import inject
from sqlalchemy import func

from domain.page.HtmlTemplateService import HtmlTemplateService, Pagination
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.operation import DataOperationJob, DataOperation, DataOperationJobExecution, \
    DataOperationJobExecutionIntegration, DataOperationJobExecutionIntegrationEvent


class DataOperationJobDetailPage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render_job(self, id, pagination=None):
        headers = [
            {'value': 'Id'},
            {'value': 'JobId'},
            {'value': 'Name'},
            {'value': 'Contacts'},
            {'value': 'Next Run Time'},
            {'value': 'Cron'},
            {'value': 'Start Date'},
            {'value': 'End Date'},
            {'value': 'Creation Date'},
            {'value': 'Last Update Date'},
            {'value': 'Is Deleted'}
        ]

        def prepare_row(data):
            data_operation_job = data.DataOperationJob
            last_update_date = None
            if data_operation_job.LastUpdatedDate is not None:
                last_update_date = data_operation_job.LastUpdatedDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            next_run_time = '-'
            if data_operation_job.ApSchedulerJob is not None and data_operation_job.ApSchedulerJob.NextRunTime is not None:
                next_run_time = data_operation_job.ApSchedulerJob.NextRunTime
            contacts = []
            if data_operation_job.DataOperation.Contacts is not None and len(
                    data_operation_job.DataOperation.Contacts) > 0:
                for contact in data_operation_job.DataOperation.Contacts:
                    contacts.append(contact.Email)
            contact_str = ';'.join(contacts)
            row = {
                "data": [
                    {'value': f'<a href="/DataOperation/Job/{data_operation_job.Id}">{data_operation_job.Id}</a>'},
                    {'value': data_operation_job.ApSchedulerJobId},
                    {
                        'value': f'<a href="/DataOperation/{data_operation_job.DataOperation.Id}">{data_operation_job.DataOperation.Name}({data_operation_job.DataOperation.Id})</a>'},
                    {'value': contact_str},
                    {'value': next_run_time},
                    {'value': data_operation_job.Cron},
                    {'value': data_operation_job.StartDate},
                    {'value': data_operation_job.EndDate},
                    {'value': data_operation_job.CreationDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                     'class': 'row-nowrap'},
                    {'value': last_update_date, 'class': 'row-nowrap'},
                    {'value': data_operation_job.IsDeleted},

                ]
            }
            return row

        data_operation_repository = self.repository_provider.get(DataOperationJob)

        query = data_operation_repository.database_session_manager.session.query(DataOperationJob,
                                                                                 DataOperation.Name).join(
            DataOperationJob.DataOperation).filter(DataOperationJob.Id == id)
        # if pagination.Filter is not None and pagination.Filter != '':
        #     if pagination.Filter == '0':
        #         query = query.filter(DataOperationJob.Cron != None)
        #         query = query.filter(DataOperationJob.IsDeleted == 0)
        #     elif pagination.Filter == '1':
        #         query = query.filter(DataOperationJob.Cron != None)
        #     elif pagination.Filter == '2':
        #         query = query.filter(DataOperationJob.IsDeleted == 0)
        #     else:
        #         query = query.filter(DataOperation.Name.ilike(f'%{pagination.Filter}%'))
        # job_execution_integrations = job_execution_integrations_query.all()
        # pagination.PageUrl = '/DataOperation/Job{}'
        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           sortable='"DataOperationJob"."Id" desc',
                                                                           pagination=pagination)

        table = self.html_template_service.render_table(source=table_data)
        return self.html_template_service.render_html(content=table)

    def render_job_execution(self, job_id, pagination):
        headers = [
            {'value': 'Execution Id'},
            {'value': 'Job Id'},
            {'value': 'Name'},
            {'value': 'Schedule Info'},
            {'value': 'Status'},
            {'value': 'Error'},
            {'value': 'Source Data Count'},
            {'value': 'Affected Row Count'},
            {'value': 'Execution Start Date'},
            {'value': 'Execution End Date'}
        ]

        def prepare_row(data: DataOperationJobExecution):
            # data_operation_job = data.DataOperationJob
            # last_update_date = None
            # if data_operation_job.LastUpdatedDate is not None:
            #     last_update_date = data_operation_job.LastUpdatedDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            # next_run_time = '-'
            # if data_operation_job.ApSchedulerJob is not None and data_operation_job.ApSchedulerJob.NextRunTime is not None:
            #     next_run_time = data_operation_job.ApSchedulerJob.NextRunTime
            # contacts = []
            # if data_operation_job.DataOperation.Contacts is not None and len(
            #         data_operation_job.DataOperation.Contacts) > 0:
            #     for contact in data_operation_job.DataOperation.Contacts:
            #         contacts.append(contact.Email)
            # contact_str = ';'.join(contacts)
            max_id = self.repository_provider.database_session_manager.session.query(
                func.max(DataOperationJobExecutionIntegration.Id)) \
                .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == data.Id)
            error_integration = self.repository_provider.get(DataOperationJobExecutionIntegration).first(Id=max_id)
            error_log = ''
            if error_integration is not None and error_integration.Log is not None:
                error_log = error_integration.Log.replace('\n', '<br />').replace('\t',
                                                                                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            total_source_data_count = self.repository_provider.database_session_manager.session.query(
                func.sum(DataOperationJobExecutionIntegration.SourceDataCount).label("SourceDataCount")) \
                .filter(DataOperationJobExecutionIntegration.DataOperationJobExecutionId == data.Id).first()[0]
            if total_source_data_count is None or total_source_data_count < 0:
                total_source_data_count = 0

            total_affected_row = self.repository_provider.database_session_manager.session.query(
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
                         'class': 'mail-row-nowrap'},
                        {'value': end_date,
                         'class': 'mail-row-nowrap'}
                    ]
            }
            return row

        data_operation_job_execution_repository = self.repository_provider.get(DataOperationJobExecution)

        query = data_operation_job_execution_repository.filter_by(DataOperationJobId=job_id)
        pagination.PageUrl = '/DataOperation/Job/'+str(job_id)+'{}'
        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           sortable='"Id" desc',
                                                                           pagination=pagination)

        table = self.html_template_service.render_table(source=table_data)
        return self.html_template_service.render_html(content=table)

    def render(self, id, pagination: Pagination):
        if pagination is None:
            pagination = Pagination(Limit=50)
        elif pagination.Limit is None:
            pagination.Limit = 50
        table_job = self.render_job(id)
        table_job_execution = self.render_job_execution(id, pagination)
        return self.html_template_service.render_html(
            content=f'''  
            <div style="font-size: 24px;"><b>Job </b></div>
            {table_job}
            <div style="font-size: 24px;"><b>Job Executions </b></div>
            {table_job_execution}
            ''')
