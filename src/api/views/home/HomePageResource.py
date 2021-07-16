import json

from flask import make_response, request
from injector import inject

from IocManager import IocManager
from domain.home.page.HomePage import HomePage
from infrastructure.api.ResourceBase import ResourceBase
from infrastructure.json.JsonConvert import JsonConvert
from views.home.PageModels import PageModels


@PageModels.ns.route('/Home',doc=False)
class HomePageResource(ResourceBase):
    @inject
    def __init__(self, page: HomePage,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page

    @IocManager.api.representation('text/html')
    def get(self):
        data = PageModels.parser.parse_args(request)
        pagination = JsonConvert.FromJSON(json.dumps(data))
        page = self.page.render(pagination=pagination)
        return make_response(page, 200)
