from injector import inject

from domain.page.HtmlTemplateService import HtmlTemplateService
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.common import Log


class DataOperationJobExecutionLogPage(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 html_template_service: HtmlTemplateService):
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def prepare_log_table_data(self, data_operation_job_execution_id):
        log_repository = self.repository_provider.get(Log)
        logs = log_repository.filter_by(JobId=data_operation_job_execution_id)
        columns = [
            {'value': 'Date'},
            {'value': 'Comment'},
            {'value': 'Content'}
        ]
        rows = []
        for log in logs:
            row = {
                "data": [
                    {'value': log.CreationDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3], 'class': 'mail-row-nowrap'},
                    {'value': log.Comments, 'class': 'mail-row-nowrap'},
                    {'value': log.Content}
                ]
            }
            rows.append(row)
        return {'columns': columns, 'rows': rows}

    def render(self, data_operation_job_execution_id: int):
        log_table_data = self.prepare_log_table_data(
            data_operation_job_execution_id=data_operation_job_execution_id)

        log_table = self.html_template_service.render_table(columns=log_table_data['columns'],
                                                            rows=log_table_data['rows'],
                                                            width=800)
        return self.html_template_service.render_html(content=log_table)
