from injector import inject

from domain.page.HtmlTemplateService import HtmlTemplateService, Pagination
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.connection import Connection, ConnectionDatabase


class HomePage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render(self, pagination: Pagination):
        return self.html_template_service.render_html(content=f'''  <div style="font-size: 24px;"><b>Home </b></div>''')
