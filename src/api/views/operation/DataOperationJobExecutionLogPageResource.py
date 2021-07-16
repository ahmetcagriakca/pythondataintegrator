from flask import make_response
from injector import inject
from domain.operation.page.DataOperationJobExecutionLogPage import DataOperationJobExecutionLogPage
from IocManager import IocManager
from infrastructure.api.ResourceBase import ResourceBase
from views.operation.PageModels import PageModels


@PageModels.ns.route('/Job/Execution/Log/<int:data_operation_job_execution_id>',doc=False)
class DataOperationJobExecutionLogPageResource(ResourceBase):
    @inject
    def __init__(self, page: DataOperationJobExecutionLogPage,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    @IocManager.api.representation('text/html')
    def get(self, data_operation_job_execution_id):
        page = self.page.render(
            data_operation_job_execution_id=data_operation_job_execution_id)
        return make_response(page, 200)
