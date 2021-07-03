from typing import List

from injector import inject

from domain.page.HtmlTemplateService import HtmlTemplateService, Pagination
from infrastructor.data.RepositoryProvider import RepositoryProvider
from infrastructor.dependency.scopes import IScoped
from models.dao.integration import DataIntegrationConnection
from models.dao.operation import DataOperation, DataOperationIntegration
from models.enums import ConnectionTypes


class DataOperationDetailPage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render_data_operation(self, data_operation_id):
        headers = [
            {'value': 'Id'},
            {'value': 'Name'},
            {'value': 'Contacts'},
            {'value': 'Definition Id'},
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
                definition_url = f'<a href="/DataOperation/Definition/{data.DefinitionId}">{data.DefinitionId}</a>'
            contacts = []
            if data.Contacts is not None and len(data.Contacts) > 0:
                for contact in data.Contacts:
                    contacts.append(contact.Email)
            contact_str = ','.join(contacts)
            row = {
                "data": [
                    {'value': data.Id},
                    {'value': data.Name},
                    {'value': contact_str},
                    {'value': definition_url},
                    {'value': data.CreationDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3], 'class': 'row-nowrap'},
                    {'value': last_update_date, 'class': 'row-nowrap'},
                    {'value': data.IsDeleted, 'class': 'row-nowrap'},
                ]
            }
            return row

        data_operation_repository = self.repository_provider.get(DataOperation)
        query = data_operation_repository.filter_by(Id=data_operation_id)

        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           pagination=None)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def render_data_operation_integration(self, data_operation_id):
        headers = [
            {'value': 'Id'},
            {'value': 'Order'},
            {'value': 'Name'},
            {'value': 'Limit'},
            {'value': 'Process'},
            {'value': 'Source Connection'},
            {'value': 'Target Connection'},
            {'value': 'Source Query'},
            {'value': 'Target Query'},
            {'value': 'IsTargetTruncate'},
            {'value': 'Comments'},
            {'value': 'Create Date'},
        ]

        def prepare_row(data: DataOperationIntegration):
            data_integration_connections: List[DataIntegrationConnection] = data.DataIntegration.Connections
            source_connections = [data_integration_connection for data_integration_connection in
                                  data_integration_connections if
                                  data_integration_connection.IsDeleted == 0 and data_integration_connection.SourceOrTarget == 0]
            target_connections = [data_integration_connection for data_integration_connection in
                                  data_integration_connections if
                                  data_integration_connection.IsDeleted == 0 and data_integration_connection.SourceOrTarget == 1]
            source_connection_text = ''
            source_query = ''
            if source_connections is not None and len(source_connections) > 0:
                source_connection = source_connections[0]
                if source_connection.Connection.ConnectionType.Name == ConnectionTypes.Database.name:
                    source_schema_and_table = ''
                    if source_connection.Database.Schema is not None and source_connection.Database.Schema != '':
                        source_schema_and_table = f' ({source_connection.Database.Schema}.{source_connection.Database.TableName})'
                    connection_url = f'<a href="/Connection/{source_connection.Connection.Id}">{source_connection.Connection.Name}</a>'
                    source_connection_text = f'{connection_url}-{source_connection.Connection.Database.ConnectorType.Name}{source_schema_and_table}'
                    source_query=''
                    if source_connection.Database.Query is not None:
                        source_query = source_connection.Database.Query.replace('\n', '<br />').replace('\t',
                                                                                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
            target_connection_text = ''

            target_query = ''
            if target_connections is not None and len(target_connections) > 0:
                target_connection = target_connections[0]
                if target_connection.Connection.ConnectionType.Name == ConnectionTypes.Database.name:
                    target_schema_and_table = ''
                    if target_connection.Database.Schema is not None and target_connection.Database.Schema != '':
                        target_schema_and_table = f' ({target_connection.Database.Schema}.{target_connection.Database.TableName})'
                    connection_url = f'<a href="/Connection/{target_connection.Connection.Id}">{target_connection.Connection.Name}</a>'
                    target_connection_text = f'{connection_url}-{target_connection.Connection.Database.ConnectorType.Name}{target_schema_and_table}'
                    target_query=''
                    if target_connection.Database.Query is not None:
                        target_query = target_connection.Database.Query.replace('\n', '<br />').replace('\t',
                                                                                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')

            row = {
                "data": [
                    {'value': data.Id},
                    {'value': data.Order},
                    {'value': data.DataIntegration.Code},
                    {'value': data.Limit},
                    {'value': data.ProcessCount},
                    {'value': source_connection_text},
                    {'value': target_connection_text},
                    {'value': source_query},
                    {'value': target_query},
                    {'value': data.DataIntegration.IsTargetTruncate},
                    {'value': data.DataIntegration.Comments},
                    {'value': data.CreationDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3], 'class': 'row-nowrap'},
                    # {'value': data.IsDeleted, 'class': 'row-nowrap'},
                ]
            }
            return row

        data_operation_integration_repository = self.repository_provider.get(DataOperationIntegration)
        query = data_operation_integration_repository.filter_by(
            DataOperationId=data_operation_id,IsDeleted=0)

        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           sortable='"Order" asc',
                                                                           pagination=None)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def render(self, data_operation_id=0, pagination: Pagination = None):
        table_data_operation = self.render_data_operation(data_operation_id=data_operation_id)
        table_data_integration_integration = self.render_data_operation_integration(
            data_operation_id=data_operation_id)

        return self.html_template_service.render_html(
            content=f'''  <div style="font-size: 24px;"><b>Data Operation </b></div>
{table_data_operation} 
<div style="font-size: 24px;"><b>Data Operation Integrations</b></div> {table_data_integration_integration}
''')
