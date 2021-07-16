import json

from flask import make_response, request
from injector import inject

from IocManager import IocManager
from domain.operation.page.DataOperationJobExecutionPage import DataOperationJobExecutionPage
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.json.JsonConvert import JsonConvert
from views.operation.PageModels import PageModels


@PageModels.ns.route('/Job/Execution',doc=False)
class DataOperationJobExecutionPageResource(ResourceBase):
    @inject
    def __init__(self, page: DataOperationJobExecutionPage,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    @IocManager.api.representation('text/html')
    def get(self):
        data = PageModels.parser.parse_args(request)
        pagination = JsonConvert.FromJSON(json.dumps(data))
        page = self.page.render(pagination=pagination)
        return make_response(page, 200)
