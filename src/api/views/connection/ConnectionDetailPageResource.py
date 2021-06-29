import json

from flask import make_response, request
from injector import inject

from domain.connection.page.ConnectionDetailPage import ConnectionDetailPage
from IocManager import IocManager
from infrastructor.api.ResourceBase import ResourceBase
from infrastructor.json.JsonConvert import JsonConvert
from views.connection.PageModels import PageModels


@PageModels.ns.route('/<int:connection_id>')
class ConnectionDetailPageResource(ResourceBase):
    @inject
    def __init__(self, page: ConnectionDetailPage,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    @IocManager.api.representation('text/html')
    def get(self,connection_id):
        data = PageModels.parser.parse_args(request)
        pagination = JsonConvert.FromJSON(json.dumps(data))
        page = self.page.render(id=connection_id,pagination=pagination)
        return make_response(page, 200)
