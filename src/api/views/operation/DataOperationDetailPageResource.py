import json

from flask import make_response, request
from injector import inject

from domain.operation.page.DataOperationDetailPage import DataOperationDetailPage
from domain.operation.page.DataOperationPage import DataOperationPage
from IocManager import IocManager
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.json.JsonConvert import JsonConvert
from views.operation.PageModels import PageModels


@PageModels.ns.route('/<int:data_operation_id>',doc=False)
class DataOperationDetailPageResource(ResourceBase):
    @inject
    def __init__(self, page: DataOperationDetailPage,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    @IocManager.api.representation('text/html')
    def get(self,data_operation_id):
        data = PageModels.parser.parse_args(request)
        pagination = JsonConvert.FromJSON(json.dumps(data))
        page = self.page.render(data_operation_id=data_operation_id,pagination=pagination)
        return make_response(page, 200)
