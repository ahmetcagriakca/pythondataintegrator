import json

from flask import make_response, request
from injector import inject

from IocManager import IocManager
from domain.operation.page.DataOperationJobDetailPage import DataOperationJobDetailPage
from domain.operation.page.DataOperationJobPage import DataOperationJobPage
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.json.JsonConvert import JsonConvert
from views.operation.PageModels import PageModels


@PageModels.ns.route('/Job/<int:data_operation_job_id>',doc=False)
class DataOperationJobDetailPageResource(ResourceBase):
    @inject
    def __init__(self, page: DataOperationJobDetailPage,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    @IocManager.api.representation('text/html')
    def get(self, data_operation_job_id):
        data = PageModels.parser.parse_args(request)
        pagination = JsonConvert.FromJSON(json.dumps(data))
        page = self.page.render(id=data_operation_job_id, pagination=pagination)
        return make_response(page, 200)
