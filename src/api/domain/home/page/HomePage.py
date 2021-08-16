from injector import inject

from infrastructure.html.HtmlTemplateService import HtmlTemplateService, Pagination
from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped


class HomePage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render(self, pagination: Pagination):
        return self.html_template_service.render_html(content=f'''  <div style="font-size: 24px;"><b>Home </b></div>''')
