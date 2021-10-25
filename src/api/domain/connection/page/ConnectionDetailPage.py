from typing import List

from injector import inject

from pdip.html import HtmlTemplateService, Pagination
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from models.dao.connection import ConnectionDatabase, Connection
from models.dao.integration import DataIntegrationConnection
from models.dao.operation import DataOperationIntegration
from models.enums import ConnectionTypes


class ConnectionDetailPage(IScoped):

    @inject
    def __init__(self, repository_provider: RepositoryProvider, html_template_service: HtmlTemplateService):
        super().__init__()
        self.repository_provider = repository_provider
        self.html_template_service = html_template_service

    def render_connection(self, id):
        headers = [
            {'value': 'Id'},
            {'value': 'Name'},
            {'value': 'Connection Type'},
            {'value': 'Connector Type'},
            {'value': 'Host'},
            {'value': 'Port'},
            {'value': 'Sid'},
            {'value': 'Service Name'},
            {'value': 'Database Name'},
            {'value': 'Creation Date'},
            {'value': 'Last Update Date'}
        ]

        def prepare_row(data):
            connection: Connection = data.Connection
            connection_database: ConnectionDatabase = data.ConnectionDatabase
            last_update_date = None
            if connection_database.LastUpdatedDate is not None:
                last_update_date = connection_database.LastUpdatedDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3]
            row = {
                "data": [
                    {'value': f'<a href="/Connection/{connection.Id}">{connection.Id}</a>'},
                    {'value': connection.Name},
                    {'value': connection.ConnectionType.Name},
                    {'value': connection_database.ConnectorType.Name},
                    {'value': connection.ConnectionServers[0].Host},
                    {'value': connection.ConnectionServers[0].Port},
                    {'value': connection_database.Sid},
                    {'value': connection_database.ServiceName},
                    {'value': connection_database.DatabaseName},
                    {'value': connection_database.CreationDate.strftime('%d.%m.%Y-%H:%M:%S.%f')[:-3],
                     'class': 'row-nowrap'},
                    {'value': last_update_date, 'class': 'row-nowrap'},
                ]
            }
            return row

        query = self.repository_provider.create().session.query(
            ConnectionDatabase, Connection
        ) \
            .filter(ConnectionDatabase.ConnectionId == Connection.Id) \
            .filter(Connection.Id == id) \
            .filter(ConnectionDatabase.IsDeleted == 0)
        # job_execution_integrations = job_execution_integrations_query.all()
        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def render_connection_detail(self, id):
        headers = [
            {'value': 'Id'},
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
                    source_connection_text = f'{source_connection.Connection.Name}-{source_connection.Connection.Database.ConnectorType.Name}{source_schema_and_table}'
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
                    target_connection_text = f'{target_connection.Connection.Name}-{target_connection.Connection.Database.ConnectorType.Name}{target_schema_and_table}'
                    target_query = target_connection.Database.Query.replace('\n', '<br />').replace('\t',
                                                                                                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')

            row = {
                "data": [
                    {'value': data.Id},
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
                ]
            }
            return row

        data_operation_integration_repository = self.repository_provider.get(DataOperationIntegration)
        query = data_operation_integration_repository.filter_by(IsDeleted=0,
                                                                DataOperationId=id)

        table_data = self.html_template_service.prepare_table_data_dynamic(query=query,
                                                                           headers=headers,
                                                                           prepare_row=prepare_row,
                                                                           pagination=None)

        table = self.html_template_service.render_table(source=table_data)
        return table

    def render(self, id=0, pagination: Pagination = None):
        table_connection = self.render_connection(id=id)
        table_connection_detail = ''
        # self.render_connection_detail(            id=id)

        return self.html_template_service.render_html(
            content=f'''  <div style="font-size: 24px;"><b>Connection </b></div>{table_connection}  {table_connection_detail}''')
