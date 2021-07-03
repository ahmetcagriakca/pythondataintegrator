import json

from injector import inject

from domain.page.HtmlTemplateService import HtmlTemplateService, Pagination
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.operation import DataOperation, Definition


class DefinitionPage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render_data_operation(self, definition_id):
        headers = [
            {'value': 'Id'},
            {'value': 'Name'},
            {'value': 'Contacts'},
            {'value': 'Create Date'},
            {'value': 'Last Update Date'},
            {'value': 'Is Deleted'}
        ]

        def prepare_row(data: DataOperation):
            last_update_date = None
            if data.LastUpdatedDate is not None:
                last_update_date = data.LastUpdatedDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            definition_url = '-'
            if data.DefinitionId is not None:
                definition_url = f'<a href="/definition/{data.DefinitionId}">{data.DefinitionId}</a>'
            contacts = []
            if data.Contacts is not None and len(data.Contacts) > 0:
                for contact in data.Contacts:
                    contacts.append(contact.Email)
            contact_str = ','.join(contacts)
            row = {
                "data": [
                    {
                        'value': f'<a href="/DataOperation/{data.Id}">{data.Id}</a>'},
                    {
                        'value': f'<a href="/DataOperation/{data.Id}">{data.Name}</a>'},

                    {'value': contact_str},
                    {'value': data.CreationDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3], 'class': 'row-nowrap'},
                    {'value': last_update_date, 'class': 'row-nowrap'},
                    {'value': data.IsDeleted, 'class': 'row-nowrap'},
                ]
            }
            return row

        data_operation_repository = self.repository_provider.get(DataOperation)
        query = data_operation_repository.filter_by(DefinitionId=definition_id)

        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           pagination=None)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def prepare_new_version(self, data):
        new_json = {}
        new_json['Name'] = data['Name']
        new_json['Contacts'] = data['Contacts']
        new_json['Integrations'] = []
        for integrations in data['Integrations']:

            new_integrations = {}
            new_integrations['Limit'] = integrations['Limit']
            new_integrations['ProcessCount'] = integrations['ProcessCount']
            integration = integrations['Integration']
            new_integration = {}
            new_integration['Code'] = integration['Code']
            if integration['SourceConnectionName'] is not None and integration['SourceConnectionName'] != '':
                new_integration['SourceConnections'] = {}
                new_integration['SourceConnections']['ConnectionName'] = integration['SourceConnectionName']
                new_integration['SourceConnections']['Database'] = {}
                new_integration['SourceConnections']['Database']['Schema'] = integration['SourceSchema']
                new_integration['SourceConnections']['Database']['TableName'] = integration['SourceTableName']
                new_integration['SourceConnections']['Database']['Query'] = integration['SourceQuery']
                new_integration['SourceConnections']['Columns'] = integration['SourceColumns']
            new_integration['TargetConnections'] = {}
            new_integration['TargetConnections']['ConnectionName'] = integration['TargetConnectionName']
            new_integration['TargetConnections']['Database'] = {}
            new_integration['TargetConnections']['Database']['Schema'] = integration['TargetSchema']
            new_integration['TargetConnections']['Database']['TableName'] = integration['TargetTableName']
            new_integration['TargetConnections']['Database']['Query'] = integration['TargetQuery']
            new_integration['TargetConnections']['Columns'] = integration['TargetColumns']

            new_integration['IsTargetTruncate'] = integration['IsTargetTruncate']
            new_integration['IsDelta'] = integration['IsDelta']
            new_integration['Comments'] = integration['Comments']

            new_integrations['Integration'] = new_integration
            new_json['Integrations'].append(new_integrations)
        return new_json

    def render_definition(self, definition_id):
        definition_repository = self.repository_provider.get(Definition)
        query = definition_repository.first(Id=definition_id)
        content = ''
        if query.Content is not None:
            data = json.loads(query.Content)
            if 'SourceConnectionName' in data['Integrations'][0]['Integration']:
                data = self.prepare_new_version(data=data)

            content = json.dumps(data, indent=4)
            # content = json.loads(query.Content)
        return f'''
        
<pre>
<code>
{content}
</code>
</pre>
        '''

    def render(self, definition_id=0, pagination: Pagination = None):
        table_data_operation = self.render_data_operation(definition_id=definition_id)
        html_definition = self.render_definition(
            definition_id=definition_id)

        return self.html_template_service.render_html(
            content=f'''  <div style="font-size: 24px;"><b>Data Operation </b></div>
{table_data_operation} 
<div style="font-size: 24px;"><b>Definition</b></div> {html_definition}
''')
