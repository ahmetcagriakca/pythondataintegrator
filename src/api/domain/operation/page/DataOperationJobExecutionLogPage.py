from injector import inject

from pdip.html import HtmlTemplateService, Pagination
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from models.dao.common import Log


class DataOperationJobExecutionLogPage(IScoped):
    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

        self.headers = [
            {'value': 'Date'},
            {'value': 'Comment'},
            {'value': 'Content'}
        ]

    def prepare_data_operation_row(self, data):
        content=''

        if data is not None and data.Content is not None:
            content = data.Content.replace('\n', '<br />').replace('\t',
                                                                              '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        row = {
            "data": [
                {'value': data.CreationDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3], 'class': 'row-nowrap'},
                {'value': data.Comments, 'class': 'row-nowrap'},
                {'value': content}
            ]
        }
        return row

    def render(self, data_operation_job_execution_id: int, pagination: Pagination = None):
        log_repository = self.repository_provider.get(Log)
        query = log_repository.filter_by(JobId=data_operation_job_execution_id)

        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=self.headers,
                                                                           prepare_row=self.prepare_data_operation_row,
                                                                           sortable='"Id" asc',
                                                                           pagination=None)

        table = self.html_template_service.render_table(source=table_data
                                                        )


        return self.html_template_service.render_html(
            content=f'''  <div style="font-size: 24px;"><b>Job Execution Logs </b></div>{table}''')

