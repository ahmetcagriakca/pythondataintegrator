from injector import inject
from pdip.data.repository import RepositoryProvider
from pdip.dependency import IScoped
from pdip.html import HtmlTemplateService, Pagination

from src.domain.operation import DataOperation


class DataOperationPage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render_data_operation(self, pagination):
        headers = [
            {'value': 'Id'},
            {'value': 'Name'},
            {'value': 'Contacts'},
            {'value': 'Definition Id'},
            {'value': 'Create Date'},
            {'value': 'Last Update Date'}
        ]

        def prepare_row(data: DataOperation):
            last_update_date = None
            if data.LastUpdatedDate is not None:
                last_update_date = data.LastUpdatedDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            definition_url = '-'
            if data.DefinitionId is not None:
                definition_url = f'<a href="/DataOperation/Definition/{data.DefinitionId}">{data.DefinitionId}</a>'
            contacts = []
            if data.Contacts is not None and len(data.Contacts) > 0:
                for contact in data.Contacts:
                    contacts.append(contact.Email)
            contact_str = ','.join(contacts)
            row = {
                "data": [
                    {'value': f'<a href="/DataOperation/{data.Id}">{data.Id}</a>'},
                    {'value': data.Name},
                    {'value': contact_str},
                    {'value': definition_url},
                    {'value': data.CreationDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3], 'class': 'row-nowrap'},
                    {'value': last_update_date, 'class': 'row-nowrap'},

                ]
            }
            return row

        data_operation_repository = self.repository_provider.get(DataOperation)
        query = data_operation_repository.filter_by(IsDeleted=0)

        pagination.PageUrl = '/DataOperation{}'

        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           sortable='"Id" desc',
                                                                           pagination=pagination)

        table = self.html_template_service.render_table(source=table_data
                                                        )
        return table

    def render(self, pagination: Pagination):
        table_data_operation = self.render_data_operation(pagination)
        return self.html_template_service.render_html(content=f'''
        
                    <div style="font-size: 24px;"><b>Data Operations </b></div>
{table_data_operation}''')
