import json

from injector import inject

from infrastructure.html.HtmlTemplateService import HtmlTemplateService, Pagination
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from models.dao.operation import DataOperationJob, DataOperation


class DataOperationJobPage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render_job(self, pagination):
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
            {'value': 'Is Deleted'},
            {'value': 'Definition'}
        ]

        def prepare_row(data):
            data_operation_job = data.DataOperationJob
            last_update_date = None
            if data_operation_job.LastUpdatedDate is not None:
                last_update_date = data_operation_job.LastUpdatedDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            next_run_time = '-'
            if data_operation_job.ApSchedulerJob is not None and data_operation_job.ApSchedulerJob.NextRunTime is not None:
                next_run_time = data_operation_job.ApSchedulerJob.NextRunTime
            contacts=[]
            if data_operation_job.DataOperation.Contacts is not None and len(data_operation_job.DataOperation.Contacts)>0:
                for contact in data_operation_job.DataOperation.Contacts:
                    contacts.append(contact.Email)
            contact_str=';'.join(contacts)
            op_def=''
            if data_operation_job.Cron is not None:
                definition={
                    "OperationName":data_operation_job.DataOperation.Name,
                    "Cron":data_operation_job.Cron
                }
            # else:
            #     definition={
            #         "OperationName":data_operation_job.DataOperation.Name,
            #         "RunDate":data_operation_job.StartDate
            #     }
                op_def=json.dumps(definition,indent=4)
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
                    {'value': f'''{op_def}'''},

                ]
            }
            return row


        query = self.repository_provider.query(DataOperationJob,
                                                                                 DataOperation.Name).join(
            DataOperationJob.DataOperation)
        if pagination.Filter is not None and pagination.Filter != '':
            if pagination.Filter == '0':
                query = query.filter(DataOperationJob.Cron != None)
                query = query.filter(DataOperationJob.IsDeleted == 0)
            elif pagination.Filter == '1':
                query = query.filter(DataOperationJob.Cron != None)
            elif pagination.Filter == '2':
                query = query.filter(DataOperationJob.IsDeleted == 0)
            else:
                query = query.filter(DataOperation.Name.ilike(f'%{pagination.Filter}%'))
        # job_execution_integrations = job_execution_integrations_query.all()
        pagination.PageUrl = '/DataOperation/Job{}'
        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           sortable='"DataOperationJob"."Id" desc',
                                                                           pagination=pagination)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def render(self, pagination: Pagination):
        if pagination is None:
            pagination = Pagination(Limit=50)
        elif pagination.Limit is None:
            pagination.Limit = 50
        table_job = self.render_job(pagination)
        return self.html_template_service.render_html(
            content=f'''  <div style="font-size: 24px;"><b>Jobs </b></div>{table_job}''')
