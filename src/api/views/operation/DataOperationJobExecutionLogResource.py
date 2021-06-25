from flask import make_response
from injector import inject
from domain.operation.page.DataOperationJobExecutionLogPage import DataOperationJobExecutionLogPage
from IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase

ns = IocManager.api.namespace('DataOperation', description='Data Operation endpoints',
                              path='/DataOperation/Job/Execution/Log')


@ns.route('/<int:data_operation_job_execution_id>', doc=False)
class DataOperationJobExecutionLogResource(ResourceBase):
    @inject
    def __init__(self, data_operation_job_execution_log_page: DataOperationJobExecutionLogPage,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_operation_job_execution_log_page = data_operation_job_execution_log_page

    @IocManager.api.representation('text/html')
    def get(self, data_operation_job_execution_id):
        page = self.data_operation_job_execution_log_page.render(
            data_operation_job_execution_id=data_operation_job_execution_id)
        return make_response(page, 200)
